# API Testing Guide

## Prerequisites

Make sure the server is running:
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

Server should be running at: http://localhost:8000

---

## Method 1: Swagger UI (Easiest - Web Interface)

### Step 1: Open Swagger UI
Open in your browser: http://localhost:8000/api/schema/swagger-ui/

### Step 2: Register a User
1. Find **POST /api/auth/register/** endpoint
2. Click **"Try it out"**
3. Enter request body:
```json
{
  "email": "test@example.com",
  "name": "Test User",
  "password": "testpass123",
  "password_confirm": "testpass123"
}
```
4. Click **"Execute"**
5. Copy the **access** token from the response

### Step 3: Authorize
1. Click the green **"Authorize"** button (top right)
2. Enter: `Bearer <your_access_token>`
3. Click **"Authorize"** then **"Close"**

### Step 4: Test Endpoints
Now you can test any endpoint! Try these:

#### List Products
- Find **GET /api/products/**
- Click "Try it out" → "Execute"

#### Create a Product (requires admin)
- Find **POST /api/products/**
- Click "Try it out"
- Enter:
```json
{
  "name": "Mleko 1L",
  "points": 10,
  "status": "ACTIVE"
}
```
- Click "Execute"

#### Get Points Balance
- Find **GET /api/points/balance/**
- Click "Try it out" → "Execute"

---

## Method 2: cURL (Command Line)

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

Save the access token from response!

### 2. Login (if already registered)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 3. Get User Profile
```bash
TOKEN="your_access_token_here"

curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. List Products
```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Create a Product (Admin only)
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mleko 1L",
    "points": 10,
    "status": "ACTIVE"
  }'
```

### 6. Search Products
```bash
curl -X GET "http://localhost:8000/api/products/search/?q=mleko" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Get Points Balance
```bash
curl -X GET http://localhost:8000/api/points/balance/ \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Scan Receipt (Mock)
```bash
curl -X POST http://localhost:8000/api/receipts/scan/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_data": "https://suf.purs.gov.rs/v/?vl=test123"
  }'
```

### 9. Submit Product for Review
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Unknown Product",
    "receipt_data": {"quantity": 1, "price": 150.0}
  }'
```

### 10. Webshop API - Get Points
```bash
API_KEY="your_api_key_here"

curl -X GET "http://localhost:8000/api/points/get/?user_id=USER_ID" \
  -H "Authorization: Bearer $API_KEY"
```

---

## Method 3: Postman / Insomnia

### Import OpenAPI Schema
1. Open Postman
2. File → Import
3. Use this URL: http://localhost:8000/api/schema/
4. All endpoints will be imported automatically!

### Or manually:
1. Create new request
2. Set method (GET/POST/etc)
3. Enter URL: http://localhost:8000/api/...
4. Add header: `Authorization: Bearer <token>`
5. For POST/PUT: Add JSON body
6. Click Send

---

## Method 4: Python Script

Create a test file `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register/", json={
    "email": "test@example.com",
    "name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
})

print("Register:", response.status_code)
data = response.json()
access_token = data['tokens']['access']

# Headers with token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Get profile
response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers)
print("Profile:", response.json())

# List products
response = requests.get(f"{BASE_URL}/api/products/", headers=headers)
print("Products:", response.json())

# Get points balance
response = requests.get(f"{BASE_URL}/api/points/balance/", headers=headers)
print("Points:", response.json())
```

Run it:
```bash
python test_api.py
```

---

## Method 5: Django Admin

For admin interface:

1. Create superuser:
```bash
cd backend
source venv/bin/activate
python manage.py createsuperuser
```

2. Open admin: http://localhost:8000/admin/

3. Login with superuser credentials

4. You can:
   - View all users, products, stores
   - Create/edit products
   - Approve/reject review requests
   - View transactions
   - Manage API keys

---

## Common Testing Scenarios

### Scenario 1: New User Flow
1. Register user → Get token
2. List products → See available products
3. Add favorite store
4. Scan receipt → Earn points
5. Check points balance

### Scenario 2: Admin Flow
1. Login as admin
2. Create products with points
3. View review requests
4. Approve/reject requests
5. View transactions

### Scenario 3: Webshop Integration
1. Create API key in Django Admin
2. Use API key to get user points
3. Deduct points during checkout
4. Add promotional points

---

## Sample Test Data

### Products
```json
[
  {"name": "Mleko 1L", "points": 10, "status": "ACTIVE"},
  {"name": "Hleb 500g", "points": 5, "status": "ACTIVE"},
  {"name": "Jogurt 150g", "points": 3, "status": "ACTIVE"},
  {"name": "Voda 2L", "points": 7, "status": "ACTIVE"}
]
```

### Stores
```json
[
  {"name": "Maxi", "location": "Beograd, Novi Beograd"},
  {"name": "Idea", "location": "Beograd, Voždovac"},
  {"name": "Roda", "location": "Novi Sad, Centar"}
]
```

---

## Troubleshooting

### 401 Unauthorized
- Token expired or invalid
- Get new token by logging in again

### 403 Forbidden
- Endpoint requires admin permissions
- Create admin user or use admin account

### 404 Not Found
- Check URL is correct
- Server might not be running

### 500 Internal Server Error
- Check server logs
- Database might not be running
- Run migrations: `python manage.py migrate`

### Connection Refused
- Server not running
- Start server: `python manage.py runserver`
- Check if port 8000 is available

---

## Quick Test Checklist

- [ ] Server running on http://localhost:8000
- [ ] Swagger UI accessible
- [ ] Can register new user
- [ ] Can login and get token
- [ ] Can list products
- [ ] Can create product (as admin)
- [ ] Can get points balance
- [ ] Can submit review request
- [ ] Admin panel accessible
- [ ] Can approve review in admin

---

## Need Help?

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **API Docs**: See `backend/API_ENDPOINTS.md`
- **Server Logs**: Check terminal where `runserver` is running
