# Loyalty App Backend - Django REST API

## Prerequisites

Before running the backend, you need to install Python dependencies.

### Install Python packages (Ubuntu/WSL)

```bash
# Install pip and venv
sudo apt update
sudo apt install python3-pip python3.12-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Database Setup

The PostgreSQL database is already configured in docker-compose.yml:

```bash
# Start PostgreSQL
docker-compose up -d

# Run migrations
python manage.py migrate

# Create superuser for Django Admin
python manage.py createsuperuser
```

## Running the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# API will be available at:
# - Swagger UI: http://localhost:8000/api/schema/swagger-ui/
# - ReDoc: http://localhost:8000/api/schema/redoc/
# - Django Admin: http://localhost:8000/admin/
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT token)
- `POST /api/auth/refresh/` - Refresh JWT token

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (admin)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (admin)
- `DELETE /api/products/{id}/` - Delete product (admin)

### Receipts
- `POST /api/receipts/scan/` - Scan and process receipt

### Transactions
- `GET /api/transactions/` - Get user transaction history
- `GET /api/transactions/{id}/` - Get transaction details

### Review Requests
- `GET /api/reviews/` - List review requests (admin)
- `POST /api/reviews/request/` - Submit product for review
- `PUT /api/reviews/{id}/approve/` - Approve review (admin)
- `PUT /api/reviews/{id}/reject/` - Reject review (admin)

### Webshop API (Mock)
- `GET /api/points/get/` - Get user points balance
- `POST /api/points/use/` - Deduct points
- `POST /api/points/add/` - Add points

### Stores
- `GET /api/stores/` - List all stores
- `POST /api/stores/favorite/` - Mark store as favorite
- `DELETE /api/stores/favorite/{id}/` - Remove favorite store
