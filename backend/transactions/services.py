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
    def extract_invoice_params(receipt_url: str) -> Optional[Dict]:
        """
        Extract invoice number and token from the receipt URL.
        The HTML page contains these in JavaScript within script tags:
        - viewModel.InvoiceNumber('M4XG7WCS-M4XG7WCS-56123')
        - viewModel.Token('8e9b6f78-3747-4929-ad10-0f3fe5391755')

        Invoice number can also be found in element with id="invoiceNumberLabel"
        """
        try:
            from bs4 import BeautifulSoup
            import re

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(receipt_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            invoice_number = None
            token = None

            # Method 1: Look for viewModel.InvoiceNumber() and viewModel.Token() in script tags
            scripts = soup.find_all('script', type='text/javascript')
            for script in scripts:
                if script.string:
                    # Match: viewModel.InvoiceNumber('M4XG7WCS-M4XG7WCS-56123')
                    inv_match = re.search(r'viewModel\.InvoiceNumber\(["\']([^"\']+)["\']\)', script.string)
                    if inv_match:
                        invoice_number = inv_match.group(1)
                        print(f"Found invoice number in viewModel: {invoice_number}")

                    # Match: viewModel.Token('8e9b6f78-3747-4929-ad10-0f3fe5391755')
                    token_match = re.search(r'viewModel\.Token\(["\']([^"\']+)["\']\)', script.string)
                    if token_match:
                        token = token_match.group(1)
                        print(f"Found token in viewModel: {token[:20]}...")

                    # Break if both found
                    if invoice_number and token:
                        break

            # Method 2: Look for invoice number in element with id="invoiceNumberLabel"
            if not invoice_number:
                inv_label = soup.find(id='invoiceNumberLabel')
                if inv_label:
                    invoice_number = inv_label.get_text(strip=True)
                    print(f"Found invoice number in label: {invoice_number}")

            # Method 3: Fallback - look for any invoiceNumber patterns
            if not invoice_number:
                all_scripts = soup.find_all('script')
                for script in all_scripts:
                    if script.string:
                        inv_match = re.search(r'invoiceNumber["\']?\s*[:=]\s*["\']([^"\']+)', script.string, re.IGNORECASE)
                        if inv_match:
                            invoice_number = inv_match.group(1)
                            print(f"Found invoice number (fallback): {invoice_number}")
                            break

            # Method 4: Fallback - look for any token patterns
            if not token:
                all_scripts = soup.find_all('script')
                for script in all_scripts:
                    if script.string:
                        token_match = re.search(r'token["\']?\s*[:=]\s*["\']([a-f0-9\-]{36})', script.string, re.IGNORECASE)
                        if token_match:
                            token = token_match.group(1)
                            print(f"Found token (fallback): {token[:20]}...")
                            break

            if invoice_number and token:
                print(f"Successfully extracted invoice params - Number: {invoice_number}, Token: {token[:20]}...")
                return {
                    'invoiceNumber': invoice_number,
                    'token': token
                }

            print(f"Could not extract invoice parameters from HTML")
            print(f"Invoice number found: {invoice_number is not None}")
            print(f"Token found: {token is not None}")
            return None

        except Exception as e:
            print(f"Error extracting invoice params: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def fetch_receipt_data(receipt_url: str) -> Optional[Dict]:
        """
        Fetch receipt data from Serbian fiscal system.

        The SUF system requires a two-step process:
        1. GET the receipt page to extract invoiceNumber and token
        2. POST to /specifications endpoint with these parameters
        """
        try:
            # Step 1: Extract invoice parameters from the receipt page
            params = ReceiptProcessingService.extract_invoice_params(receipt_url)
            if not params:
                print("Failed to extract invoice parameters from receipt URL")
                return None

            # Step 2: POST to specifications endpoint
            specifications_url = "https://suf.purs.gov.rs/specifications"

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://suf.purs.gov.rs',
                'Referer': receipt_url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            # Prepare form data
            form_data = {
                'invoiceNumber': params['invoiceNumber'],
                'token': params['token']
            }

            print(f"Posting to specifications endpoint...")
            response = requests.post(
                specifications_url,
                headers=headers,
                data=form_data,
                timeout=10
            )
            response.raise_for_status()

            print(f"Specifications response status: {response.status_code}")
            print(f"Response content type: {response.headers.get('Content-Type')}")
            print(f"Response preview: {response.text[:500]}")

            # Parse JSON response
            receipt_data = response.json()
            return receipt_data

        except requests.RequestException as e:
            print(f"Error fetching receipt data: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return None

    @staticmethod
    def parse_receipt_items(receipt_data: Dict) -> List[Dict]:
        """
        Parse items from Serbian fiscal receipt data from SUF /specifications endpoint.

        Expected JSON structure:
        {
            "success": true,
            "items": [
                {
                    "gtin": "8600115405206",
                    "name": "Cigarete Terea Oasis pearl/KOM",
                    "quantity": 1,
                    "total": 380,
                    "unitPrice": 380,
                    "label": "Ђ",
                    "labelRate": 20,
                    "taxBaseAmount": 316.67,
                    "vatAmount": 63.33
                }
            ]
        }
        """
        items = []

        # Check if the response is successful
        if not receipt_data.get('success'):
            print(f"Receipt data success=False: {receipt_data}")
            return items

        # Get items array from the response
        raw_items = receipt_data.get('items', [])

        print(f"Parsing {len(raw_items)} items from receipt data")

        for item in raw_items:
            parsed_item = {
                'name': item.get('name', 'Unknown Product'),
                'quantity': item.get('quantity', 1),
                'total': float(item.get('total', 0.0)),  # Total price for all quantities
                'unit_price': float(item.get('unitPrice', 0.0)),  # Price per unit
                'gtin': item.get('gtin', ''),  # Barcode/GTIN
            }
            print(f"  - {parsed_item['name']}: {parsed_item['quantity']}x @ {parsed_item['unit_price']} = {parsed_item['total']}")
            items.append(parsed_item)

        return items

    @staticmethod
    def extract_store_info(receipt_url: str) -> Dict:
        """
        Extract store information from the SUF receipt HTML page.
        Store info is in HTML elements with specific IDs:
        - tinLabel: PIB (Tax ID)
        - shopFullNameLabel: Store name
        - addressLabel: Address
        - cityLabel: City
        """
        try:
            from bs4 import BeautifulSoup

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(receipt_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            # Extract PIB (Tax ID Number)
            tin_elem = soup.find(id='tinLabel')
            tin = tin_elem.get_text(strip=True) if tin_elem else ''

            # Extract store name
            shop_name_elem = soup.find(id='shopFullNameLabel')
            shop_name = shop_name_elem.get_text(strip=True) if shop_name_elem else 'Unknown Store'

            # Extract address
            address_elem = soup.find(id='addressLabel')
            address = address_elem.get_text(strip=True) if address_elem else ''

            # Extract city
            city_elem = soup.find(id='cityLabel')
            city = city_elem.get_text(strip=True) if city_elem else ''

            # Combine address and city for location
            location = f"{address}, {city}" if address and city else address or city

            print(f"Extracted store info - Name: {shop_name}, TIN: {tin}, Location: {location}")

            return {
                'name': shop_name,
                'location': location,
                'tin': tin,
            }

        except Exception as e:
            print(f"Error extracting store info: {e}")
            return {
                'name': 'Unknown Store',
                'location': '',
                'tin': '',
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

        # TESTING MODE: If QR data starts with "TEST:", use mock data
        if qr_data.startswith("TEST:"):
            return cls.process_mock_receipt(qr_data, user)

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

        # Extract store information from the HTML page
        store_info = cls.extract_store_info(receipt_url)

        # Get or create store
        store, created = Store.objects.get_or_create(
            name=store_info['name'],
            defaults={'location': store_info['location']}
        )

        # Match products and calculate points
        products_db = Product.objects.all()
        matched_items = []
        total_points = 0
        total_amount = 0.0

        for item in items:
            matched_product, points = cls.match_product_by_name(item['name'], products_db)

            matched_items.append({
                'product_name': item['name'],
                'quantity': item['quantity'],
                'price': item['total'],  # Total price for this line item
                'unit_price': item['unit_price'],  # Price per unit
                'matched': matched_product is not None,
                'product_id': matched_product.id if matched_product else None,
                'points': points * item['quantity']
            })

            total_points += points * item['quantity']
            total_amount += item['total']

        # Create transaction
        transaction = Transaction.objects.create(
            user=user,
            store=store,
            total_points=total_points,
            total_amount=total_amount,
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
                unit_price=item_data['unit_price'],
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

    @classmethod
    def process_mock_receipt(cls, qr_data: str, user) -> Dict:
        """
        Process a mock receipt for testing purposes.
        QR data format: TEST:store_name:item1_name:item1_qty:item1_price,item2_name:item2_qty:item2_price
        Example: TEST:Maxi:Mleko:2:150.00,Hleb:1:80.00
        """
        from products.models import Product, Store
        from .models import Transaction, TransactionItem
        import random

        try:
            # Parse mock QR data
            parts = qr_data.split(':')
            if len(parts) < 3:
                # Simple test mode - create random receipt
                store_name = "Test Store"
                items = [
                    {'name': 'Test Product 1', 'quantity': 2, 'price': 150.00},
                    {'name': 'Test Product 2', 'quantity': 1, 'price': 250.00},
                ]
            else:
                store_name = parts[1]
                items = []
                # Parse items (format: name:qty:price)
                for item_str in parts[2:]:
                    item_parts = item_str.split(',')
                    for item_part in item_parts:
                        item_data = item_part.split(':')
                        if len(item_data) >= 3:
                            items.append({
                                'name': item_data[0],
                                'quantity': int(item_data[1]),
                                'price': float(item_data[2])
                            })

            # Get or create test store
            store, _ = Store.objects.get_or_create(
                name=store_name,
                defaults={'location': 'Test Location'}
            )

            # Match products
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

            # Create transaction with unique test URL
            test_url = f"TEST_{random.randint(100000, 999999)}"
            transaction = Transaction.objects.create(
                user=user,
                store=store,
                total_points=total_points,
                receipt_url=test_url,
                receipt_data={'test': True, 'original_qr': qr_data}
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
                'unmatched_items': [item for item in matched_items if not item['matched']],
                'test_mode': True
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing mock receipt: {str(e)}'
            }
