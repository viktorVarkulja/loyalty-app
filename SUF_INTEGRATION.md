# Serbian Fiscal Receipt (SUF) Integration

## Overview

This document explains how Serbian fiscal receipt scanning works with the SUF (Sistem za Upravljanje Fakturama) system.

## SUF System

The Serbian Tax Authority provides a receipt verification system at https://suf.purs.gov.rs that allows customers to verify fiscal receipts by scanning QR codes.

### QR Code Format

Serbian fiscal receipts contain QR codes with URLs in this format:
```
https://suf.purs.gov.rs/v/?vl=<encoded-data>
```

The `vl` parameter contains Base64-encoded receipt data.

### Receipt Data Access

The SUF system provides three ways to access receipt data:

1. **Web Interface** - Visit the URL in a browser to see HTML page with receipt details
2. **JSON API** - (Under investigation) May require specific headers or endpoint paths
3. **URL Decoding** - The `vl` parameter can be decoded offline to extract basic info

## Current Implementation

### Testing Mode (Recommended for Development)

For testing and demonstration purposes, use TEST mode:

**Simple test receipt:**
```
TEST:
```

This creates a random receipt with test products.

**Custom test receipt:**
```
TEST:StoreName:Product1:Qty:Price,Product2:Qty:Price
```

Example:
```
TEST:Maxi:Mleko:2:150.00,Hleb:1:80.00,Jogurt:3:90.50
```

This creates a receipt from "Maxi" store with:
- 2x Mleko (Milk) @ 150.00 RSD each
- 1x Hleb (Bread) @ 80.00 RSD
- 3x Jogurt (Yogurt) @ 90.50 RSD each

### Real SUF Receipts

The system attempts to fetch receipt data from real SUF URLs using these approaches:

1. **JSON API attempt** - Tries to fetch JSON data with appropriate headers
2. **Alternative endpoints** - Tries `/api/v/` path variations
3. **Logging** - Prints response details to Django console for debugging

**Current limitations:**
- The exact JSON API endpoint format for SUF is not publicly documented
- HTML parsing fallback is available but not fully implemented
- TEST mode provides full functionality for demonstration

## Implementation Details

### Backend Service

Location: `backend/transactions/services.py`

**Key methods:**
- `process_receipt(qr_data, user)` - Main processing method
- `process_mock_receipt(qr_data, user)` - TEST mode handler
- `fetch_receipt_data(receipt_url)` - Attempts to fetch from SUF
- `parse_receipt_items(receipt_data)` - Parses receipt items
- `match_product_by_name(product_name, products_db)` - Fuzzy matching (80% similarity)

### Product Matching

The system uses fuzzy matching to match receipt item names with products in the database:

1. **Exact match** - Case-insensitive exact name match
2. **Partial match** - One name contains the other
3. **Fuzzy match** - 80%+ similarity using difflib.SequenceMatcher

### Points Calculation

Points are awarded based on matched products:
- Each product in the database has a `points` value
- Total points = sum of (product_points × quantity) for all matched items
- Unmatched products earn 0 points but are still recorded

## Usage

### Frontend - Scan View

Users can:
1. **Scan QR code** with device camera
2. **Manual input** - Paste QR data or TEST command in textarea

### Testing the App

1. Navigate to the Scan page
2. Click "Or enter QR data manually"
3. Enter: `TEST:Maxi:Mleko:2:150,Hleb:1:80`
4. Click "Process Receipt"
5. View points earned and transaction details

### Adding Test Products

To ensure products match in TEST mode, add products via Django Admin:

```bash
python manage.py createsuperuser  # if not already created
python manage.py runserver
```

Visit http://localhost:8000/admin/ and add products with names like:
- Mleko (Milk)
- Hleb (Bread)
- Jogurt (Yogurt)
- Kafa (Coffee)
- Čokolada (Chocolate)

Set points values (e.g., 10 points per product).

## Future Improvements

### For Production Use with Real SUF Receipts:

1. **Obtain Official SUF API Documentation**
   - Contact Serbian Tax Authority for API specs
   - May require API key registration
   - Check for official developer portal

2. **Implement HTML Parsing Fallback**
   - Parse the HTML response from SUF URLs
   - Extract receipt data from table elements
   - Use BeautifulSoup4 (already installed)

3. **Implement URL Decoding**
   - Decode the `vl` parameter from Base64
   - Parse the binary data structure
   - Extract basic receipt info offline (no API call needed)

4. **Add Receipt Verification**
   - Verify receipt signatures/checksums
   - Detect duplicate scans (already implemented via unique qr_data)
   - Validate timestamp and store info

## Dependencies

Required Python packages (in `requirements.txt`):
```
requests==2.31.0
beautifulsoup4==4.14.2
lxml==6.0.2
```

## References

- Serbian Tax Authority: https://www.purs.gov.rs
- SUF Verification System: https://suf.purs.gov.rs
- SUF Documentation: https://tap.suf.purs.gov.rs/Help/
- GitHub PHP Parser: https://github.com/turanjanin/serbian-fiscal-receipts-parser

## Troubleshooting

### "No items found in receipt" Error

This error occurs when:
- Real SUF URL is used but JSON API endpoint is not accessible
- The system cannot parse the receipt data format

**Solution:** Use TEST mode for development/demonstration.

### Products Not Matching

If TEST mode shows 0 points:
- Check that products exist in database via Django Admin
- Product names must match (case-insensitive, 80% similarity)
- Ensure products have `status='ACTIVE'` and `points > 0`

### CORS Errors

If frontend shows CORS errors:
- Check `backend/config/settings.py` - `CORS_ALLOWED_ORIGINS`
- Ensure frontend dev server port is included (5173, 5179, etc.)
- Restart Django server after changing settings

## Support

For SUF API integration support, contact the Serbian Tax Authority or consult their official technical documentation.
