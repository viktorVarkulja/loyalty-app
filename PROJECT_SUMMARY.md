# Serbian Loyalty App - Backend Project Summary

## Project Overview
A PWA loyalty application that scans Serbian fiscal receipt QR codes, matches products, and awards points to users. Backend built with Django REST Framework.

## Technology Stack

### Backend
- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL 15 (Docker)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-spectacular (Swagger UI)
- **CORS**: django-cors-headers

### Key Features
- Serbian fiscal receipt integration (SUF system)
- QR code scanning and processing
- Fuzzy product matching (80% similarity)
- Points system with automatic calculation
- Admin review queue for unknown products
- Webshop API integration (mock)
- Comprehensive Django Admin interface

## Project Structure

```
StudioPresent/
├── backend/
│   ├── config/              # Django project settings
│   ├── users/               # User authentication & profiles
│   │   ├── models.py        # Custom User model
│   │   ├── views.py         # Auth endpoints
│   │   ├── webshop_views.py # Webshop API
│   │   └── admin.py         # User admin
│   ├── products/            # Products & Stores
│   │   ├── models.py        # Product, Store, ApiKey
│   │   ├── views.py         # CRUD endpoints
│   │   └── admin.py         # Product management
│   ├── transactions/        # Receipt scanning
│   │   ├── models.py        # Transaction, TransactionItem
│   │   ├── views.py         # Scan endpoints
│   │   ├── services.py      # Receipt processing logic
│   │   └── admin.py         # Transaction viewing
│   ├── reviews/             # Unknown product reviews
│   │   ├── models.py        # ReviewRequest
│   │   ├── views.py         # Review management
│   │   └── admin.py         # Review queue
│   ├── manage.py
│   ├── requirements.txt
│   └── API_ENDPOINTS.md     # Full API documentation
├── docker-compose.yml       # PostgreSQL configuration
├── schema.prisma            # Database schema
└── README.md
```

## Database Models

### Users
- Custom User model with email authentication
- Role-based access (USER, ADMIN)
- Points balance tracking

### Products & Stores
- Product catalog with point values
- Store information
- User favorite stores
- API keys for webshop integration

### Transactions
- Receipt scanning history
- Transaction items with product matching
- Receipt data storage (JSON)

### Reviews
- Unknown product review requests
- Admin approval/rejection workflow
- Points awarding on approval

## API Endpoints Summary

### Authentication (JWT)
- Register, Login, Token Refresh
- User profile management

### Products & Stores
- CRUD operations (admin-only for write)
- Product search
- Favorite stores

### Receipt Scanning
- QR code processing
- Serbian fiscal system integration
- Automatic product matching
- Points calculation

### Transactions
- Transaction history
- Points balance

### Review Requests
- Submit unknown products
- Admin approve/reject
- Bulk actions
- Statistics

### Webshop API
- Get user points
- Deduct points (checkout)
- Add points (promotions)
- API key authentication

## Key Achievements

✅ **Complete Backend Implementation** (3-day timeline)
- All core features implemented
- Full CRUD operations
- Serbian fiscal receipt integration
- Admin management interface

✅ **Security**
- JWT authentication
- API key authentication for webshop
- Role-based permissions
- CORS configuration

✅ **Documentation**
- Swagger UI auto-generated
- Comprehensive API documentation
- README files
- Code comments

✅ **Admin Features**
- Full Django Admin setup
- Bulk actions for reviews
- Transaction viewing (read-only)
- User management

## Git Commit History

1. `df8d8f1` - Initial commit: Django backend setup with models
2. `a1b1edf` - Implement JWT authentication and Swagger UI
3. `4fe43ca` - Add products and stores management endpoints
4. `c73cfda` - Add receipt scanning and transaction endpoints
5. `1ecc7fc` - Add review request endpoints for unknown products
6. `4b5b473` - Add webshop API endpoints for external integration
7. `59ace25` - Set up Django Admin for all models
8. `1a2089f` - Add comprehensive API documentation

## Access Points

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **Django Admin**: http://localhost:8000/admin/
- **API Base**: http://localhost:8000/api/

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Database
```bash
docker-compose up -d
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Start Server
```bash
python manage.py runserver
```

## Testing

1. Open Swagger UI: http://localhost:8000/api/schema/swagger-ui/
2. Register a new user via `/api/auth/register/`
3. Copy the access token
4. Click "Authorize" and enter: `Bearer <token>`
5. Test all endpoints

## Future Enhancements (Not Implemented)

- Push notifications (FCM)
- Advanced statistics and analytics
- Family/group point pooling
- Mobile app (PWA frontend)
- Production deployment configuration

## Notes

- PostgreSQL runs in Docker on port 5432
- All models use CUID-like IDs
- Receipt scanning uses Serbian SUF system
- Webshop API is mock implementation
- Time zone: Europe/Belgrade
- All timestamps in UTC

## Developer Information

- **Project**: Serbian Loyalty App Backend
- **Developer**: Viktor Varkulja
- **Email**: viktor.varkulja@gmail.com
- **Timeline**: Completed in phases over 3 days
- **Lines of Code**: ~3000+ (backend only)
- **Commits**: 8 major commits

## Status

✅ **Backend: 100% Complete**
- All required endpoints implemented
- Admin interface functional
- Documentation complete
- Tested via Swagger UI

⏳ **Frontend: Not started** (Vite + Vue 3 PWA planned)
⏳ **Deployment: Not configured**
