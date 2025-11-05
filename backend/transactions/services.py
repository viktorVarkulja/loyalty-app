"""
Service for processing Serbian fiscal receipts.
Integrates with Serbian Tax Authority (SUF) system.
"""
import re
import requests
from typing import Dict, List, Optional, Tuple
from django.conf import settings


class ReceiptProcessingService:
    """Service for processing fiscal receipt QR codes and matching products."""

    SUF_BASE_URL = "https://suf.purs.gov.rs"

    @staticmethod
    def extract_url_from_qr(qr_data: str) -> Optional[str]:
        """
        Extract URL from QR code data.
        Serbian fiscal receipts contain URLs like: https://suf.purs.gov.rs/v/?vl=...
        """
        # Check if it's already a URL
        if qr_data.startswith('http'):
            return qr_data

        # Try to extract URL from QR data
        url_pattern = r'(https?://[^\s]+)'
        match = re.search(url_pattern, qr_data)
        if match:
            return match.group(1)

        return None

    @staticmethod
    def fetch_receipt_data(receipt_url: str) -> Optional[Dict]:
        """
        Fetch receipt data from Serbian fiscal system.
        Sends request with Accept: application/json header to get JSON response.
        """
        try:
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'LoyaltyApp/1.0'
            }
            response = requests.get(receipt_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Try to parse JSON
            receipt_data = response.json()
            return receipt_data

        except requests.RequestException as e:
            print(f"Error fetching receipt data: {e}")
            return None
        except ValueError:
            print("Invalid JSON response from receipt URL")
            return None

    @staticmethod
    def parse_receipt_items(receipt_data: Dict) -> List[Dict]:
        """
        Parse items from Serbian fiscal receipt data.
        Returns list of items with name, quantity, price.
        """
        items = []

        # Serbian fiscal receipts typically have items in 'specifikacija' or 'items' field
        raw_items = receipt_data.get('specifikacija') or receipt_data.get('items') or []

        for item in raw_items:
            parsed_item = {
                'name': item.get('naziv') or item.get('name', 'Unknown Product'),
                'quantity': item.get('kolicina') or item.get('quantity', 1),
                'price': item.get('ukupnaCena') or item.get('totalPrice') or item.get('price', 0.0),
                'unit_price': item.get('jedinicnaCenaSaPDV') or item.get('unitPrice', 0.0),
            }
            items.append(parsed_item)

        return items

    @staticmethod
    def extract_store_info(receipt_data: Dict) -> Dict:
        """
        Extract store information from receipt data.
        Returns store name and location.
        """
        return {
            'name': receipt_data.get('imeProdajnogMesta') or receipt_data.get('storeName', 'Unknown Store'),
            'location': receipt_data.get('adresa') or receipt_data.get('address', ''),
            'pib': receipt_data.get('pib') or receipt_data.get('taxId', ''),
        }

    @staticmethod
    def match_product_by_name(product_name: str, products_db) -> Tuple[Optional[object], int]:
        """
        Match a product from receipt with products in database.
        Returns (matched_product, points) or (None, 0).
        Uses fuzzy matching for better results.
        """
        from products.models import Product
        from difflib import SequenceMatcher

        # Normalize product name
        normalized_name = product_name.lower().strip()

        # First, try exact match
        exact_match = products_db.filter(name__iexact=normalized_name, status='ACTIVE').first()
        if exact_match:
            return exact_match, exact_match.points

        # Try partial match (product name contains search term or vice versa)
        for product in products_db.filter(status='ACTIVE'):
            product_name_lower = product.name.lower()

            # Check if either name contains the other
            if normalized_name in product_name_lower or product_name_lower in normalized_name:
                return product, product.points

            # Use fuzzy matching
            similarity = SequenceMatcher(None, normalized_name, product_name_lower).ratio()
            if similarity > 0.8:  # 80% similarity threshold
                return product, product.points

        # No match found
        return None, 0

    @classmethod
    def process_receipt(cls, qr_data: str, user) -> Dict:
        """
        Main method to process receipt from QR code.
        Returns processed receipt data with matched products and points.
        """
        from products.models import Product, Store
        from .models import Transaction, TransactionItem

        # Extract URL from QR code
        receipt_url = cls.extract_url_from_qr(qr_data)
        if not receipt_url:
            return {
                'success': False,
                'error': 'Invalid QR code - could not extract receipt URL'
            }

        # Fetch receipt data from Serbian fiscal system
        receipt_data = cls.fetch_receipt_data(receipt_url)
        if not receipt_data:
            return {
                'success': False,
                'error': 'Could not fetch receipt data from fiscal system'
            }

        # Parse items from receipt
        items = cls.parse_receipt_items(receipt_data)
        if not items:
            return {
                'success': False,
                'error': 'No items found in receipt'
            }

        # Extract store information
        store_info = cls.extract_store_info(receipt_data)

        # Get or create store
        store, created = Store.objects.get_or_create(
            name=store_info['name'],
            defaults={'location': store_info['location']}
        )

        # Match products and calculate points
        products_db = Product.objects.all()
        matched_items = []
        total_points = 0

        for item in items:
            matched_product, points = cls.match_product_by_name(item['name'], products_db)

            matched_items.append({
                'product_name': item['name'],
                'quantity': item['quantity'],
                'price': item['price'],
                'matched': matched_product is not None,
                'product_id': matched_product.id if matched_product else None,
                'points': points * item['quantity']
            })

            total_points += points * item['quantity']

        # Create transaction
        transaction = Transaction.objects.create(
            user=user,
            store=store,
            total_points=total_points,
            receipt_url=receipt_url,
            receipt_data=receipt_data
        )

        # Create transaction items
        for item_data in matched_items:
            TransactionItem.objects.create(
                transaction=transaction,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                quantity=item_data['quantity'],
                price=item_data['price'],
                points=item_data['points'],
                matched=item_data['matched']
            )

        # Update user points
        user.points += total_points
        user.save()

        return {
            'success': True,
            'transaction_id': transaction.id,
            'store': {
                'id': store.id,
                'name': store.name,
                'location': store.location
            },
            'total_points': total_points,
            'items': matched_items,
            'unmatched_items': [item for item in matched_items if not item['matched']]
        }
