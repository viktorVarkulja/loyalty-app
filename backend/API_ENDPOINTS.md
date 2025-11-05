# Loyalty App API Endpoints

## Base URL
```
http://localhost:8000
```

## API Documentation
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **Django Admin**: http://localhost:8000/admin/

---

## Authentication Endpoints

### Register
```http
POST /api/auth/register/
```
**Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```
**Response:** User object + JWT tokens

### Login
```http
POST /api/auth/login/
```
**Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
**Response:** JWT tokens + user data

### Refresh Token
```http
POST /api/auth/token/refresh/
```
**Body:**
```json
{
  "refresh": "refresh_token_here"
}
```

### Get Profile
```http
GET /api/auth/profile/
```
**Headers:** `Authorization: Bearer <access_token>`

### Update Profile
```http
PUT /api/auth/profile/update/
PATCH /api/auth/profile/update/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "name": "Updated Name"
}
```

---

## Products Endpoints

### List Products
```http
GET /api/products/
```
**Headers:** `Authorization: Bearer <access_token>`

### Get Product
```http
GET /api/products/{id}/
```
**Headers:** `Authorization: Bearer <access_token>`

### Search Products
```http
GET /api/products/search/?q=mleko
```
**Headers:** `Authorization: Bearer <access_token>`

### Create Product (Admin Only)
```http
POST /api/products/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "name": "Mleko 1L",
  "points": 10,
  "status": "ACTIVE"
}
```

### Update Product (Admin Only)
```http
PUT /api/products/{id}/
PATCH /api/products/{id}/
```

### Delete Product (Admin Only)
```http
DELETE /api/products/{id}/
```

---

## Stores Endpoints

### List Stores
```http
GET /api/stores/
```
**Headers:** `Authorization: Bearer <access_token>`

### Get Store
```http
GET /api/stores/{id}/
```

### Create Store (Admin Only)
```http
POST /api/stores/
```
**Body:**
```json
{
  "name": "Maxi",
  "location": "Beograd, Novi Beograd"
}
```

### Favorite Stores

#### List Favorites
```http
GET /api/stores/favorites/
```

#### Add Favorite
```http
POST /api/stores/favorites/add/
```
**Body:**
```json
{
  "store_id": "store_id_here"
}
```

#### Remove Favorite
```http
DELETE /api/stores/favorites/{favorite_id}/
```

---

## Receipt Scanning & Transactions

### Scan Receipt
```http
POST /api/receipts/scan/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "qr_data": "https://suf.purs.gov.rs/v/?vl=..."
}
```
**Response:** Transaction details with matched/unmatched products

### Get Points Balance
```http
GET /api/points/balance/
```
**Headers:** `Authorization: Bearer <access_token>`

### List Transactions
```http
GET /api/transactions/
```
**Headers:** `Authorization: Bearer <access_token>`

### Get Transaction Details
```http
GET /api/transactions/{id}/
```
**Headers:** `Authorization: Bearer <access_token>`

---

## Review Requests (Unknown Products)

### Submit Product for Review
```http
POST /api/reviews/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "product_name": "Unknown Product Name",
  "receipt_data": {
    "quantity": 1,
    "price": 150.00
  }
}
```

### List Review Requests
```http
GET /api/reviews/
```
**Headers:** `Authorization: Bearer <access_token>`
- Admin: sees all requests
- User: sees only their own

### Get Review Details
```http
GET /api/reviews/{id}/
```

### Approve Review (Admin Only)
```http
POST /api/reviews/{id}/approve/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "points_awarded": 15,
  "admin_comment": "Approved - valid product"
}
```

### Reject Review (Admin Only)
```http
POST /api/reviews/{id}/reject/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
  "admin_comment": "Product not eligible for points"
}
```

### Get Review Statistics (Admin Only)
```http
GET /api/reviews/stats/
```

### Get My Reviews
```http
GET /api/reviews/my/
```
**Headers:** `Authorization: Bearer <access_token>`

### Get Pending Reviews (Admin Only)
```http
GET /api/reviews/pending/
```

---

## Webshop API (External Integration)

### Get User Points
```http
GET /api/points/get/?user_id={user_id}
```
**Headers:** `Authorization: Bearer <api_key>`

**Response:**
```json
{
  "success": true,
  "message": "Points retrieved successfully",
  "data": {
    "user_id": "c123456789",
    "email": "user@example.com",
    "points": 250
  }
}
```

### Use Points (Deduct)
```http
POST /api/points/use/
```
**Headers:** `Authorization: Bearer <api_key>`
**Body:**
```json
{
  "user_id": "c123456789",
  "points": 100,
  "order_id": "ORDER-12345"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully deducted 100 points",
  "data": {
    "user_id": "c123456789",
    "points_used": 100,
    "remaining_points": 150,
    "order_id": "ORDER-12345"
  }
}
```

### Add Points
```http
POST /api/points/add/
```
**Headers:** `Authorization: Bearer <api_key>`
**Body:**
```json
{
  "user_id": "c123456789",
  "points": 50,
  "reason": "Promotional bonus"
}
```

---

## Authentication Types

### JWT Authentication (Mobile App / Web App)
```http
Authorization: Bearer <jwt_access_token>
```

### API Key Authentication (Webshop Integration)
```http
Authorization: Bearer <api_key>
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message here"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Testing Instructions

1. **Start the server:**
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Access Swagger UI:**
   Open http://localhost:8000/api/schema/swagger-ui/

3. **Create a test user:**
   - Use `/api/auth/register/` endpoint
   - Copy the access token from response

4. **Authorize in Swagger:**
   - Click "Authorize" button in top right
   - Enter: `Bearer <your_access_token>`
   - Click "Authorize"

5. **Test endpoints:**
   - Try creating a product (admin required)
   - Try listing products
   - Try scanning a receipt (mock data)
   - Try creating a review request

6. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Access Django Admin:**
   Open http://localhost:8000/admin/

---

## Notes

- All timestamps are in UTC
- All IDs use CUID format
- Points are integer values
- Receipt scanning integrates with Serbian fiscal system (https://suf.purs.gov.rs)
- Webshop API is a mock implementation for demo purposes
