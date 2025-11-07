# 🎁 Loyalty Rewards App

A modern, full-stack loyalty rewards application that enables users to scan receipts, earn points, and redeem rewards. Built with Django REST Framework and Vue.js.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0.1-green.svg)
![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the Application](#running-the-application)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Features Guide](#-features-guide)
- [Environment Variables](#-environment-variables)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- 📱 **Receipt Scanning** - Scan Serbian fiscal receipts using QR codes
- 🎯 **Points System** - Earn points for every purchase
- 🛒 **Webshop** - Redeem points for rewards
- 🏪 **Store Management** - Track purchases across multiple stores
- ⭐ **Favorite Stores** - Mark and prioritize favorite stores
- 📊 **Transaction History** - Complete purchase history with filtering
- 🔍 **Product Matching** - Automatic and manual product matching
- 👤 **User Profiles** - Manage account and view points balance

### Admin Features
- 📈 **Admin Dashboard** - Comprehensive Django admin interface
- ✅ **Review System** - Approve/reject unmatched products
- 🏷️ **Product Management** - CRUD operations for products
- 🏬 **Store Management** - Manage store locations and details
- 👥 **User Management** - View and manage user accounts
- 📝 **Transaction Oversight** - Monitor all transactions and items

### Technical Features
- 🔐 **JWT Authentication** - Secure token-based authentication
- 🔄 **Token Refresh** - Automatic token refresh mechanism
- 📱 **PWA Support** - Installable progressive web app
- 🎨 **Responsive Design** - Mobile-first UI with Tailwind CSS
- 🚀 **REST API** - Well-documented API with Swagger/ReDoc
- 🗃️ **PostgreSQL Database** - Robust data persistence
- 📦 **Dockerized** - Easy deployment with Docker

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Authentication**: Simple JWT 5.3.1
- **Database**: PostgreSQL (via psycopg2-binary)
- **API Documentation**: drf-spectacular (Swagger/ReDoc)
- **CORS**: django-cors-headers
- **Web Scraping**: BeautifulSoup4, lxml, requests

### Frontend
- **Framework**: Vue 3.5 (Composition API)
- **Routing**: Vue Router 4.6
- **State Management**: Pinia 3.0
- **HTTP Client**: Axios 1.13
- **Styling**: Tailwind CSS 4.1
- **UI Components**: Radix Vue 1.9
- **QR Scanner**: vue-qrcode-reader 5.7
- **Build Tool**: Vite 7.1
- **PWA**: vite-plugin-pwa

### DevOps
- **Containerization**: Docker & Docker Compose
- **Environment Management**: python-dotenv
- **Database Migrations**: Django migrations

---

## 🏗 Architecture

```
loyalty-app/
├── backend/                 # Django backend
│   ├── config/             # Django settings & URLs
│   ├── users/              # User authentication & management
│   ├── products/           # Products & stores models
│   ├── transactions/       # Receipts & transaction processing
│   ├── reviews/            # Product review system
│   ├── manage.py
│   ├── requirements.txt
│   └── venv/
│
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Reusable Vue components
│   │   ├── views/         # Page components
│   │   ├── router/        # Vue Router configuration
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API service layer
│   │   └── assets/        # Static assets
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml      # Docker services configuration
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.12+
- **Node.js**: 18+ and npm
- **PostgreSQL**: 14+ (or Docker)
- **Git**: Latest version

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/viktorVarkulja/loyalty-app.git
cd loyalty-app
```

2. **Backend Setup**

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install
```

### Database Setup

**Option 1: Using Docker (Recommended)**

```bash
# From project root
docker-compose up -d
```

**Option 2: Local PostgreSQL**

```bash
# Create database
createdb loyalty_app

# Update backend/.env with your database credentials
```

**Run Migrations**

```bash
cd backend
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Optional: Load seed data
python seed_data.py
```

### Running the Application

**Backend (Terminal 1)**
```bash
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
python manage.py runserver
```
Backend will run at: http://localhost:8000

**Frontend (Terminal 2)**
```bash
cd frontend
npm run dev
```
Frontend will run at: http://localhost:5173

---

## 📁 Project Structure

### Backend Apps

#### **users/**
- Custom User model with email authentication
- JWT token generation and refresh
- User registration and login endpoints
- Points balance management
- Webshop API for points redemption

#### **products/**
- Product model with points and status
- Store model with location tracking
- User favorite stores (many-to-many)
- Product and store CRUD endpoints
- Favorite stores management

#### **transactions/**
- Transaction model for receipt scans
- TransactionItem for individual products
- Serbian fiscal receipt parsing
- Automatic product matching
- Points calculation logic

#### **reviews/**
- Review request system for unmatched products
- Admin approval/rejection workflow
- Product linking to unmatched items

### Frontend Structure

#### **views/**
- `HomeView` - Dashboard with points balance
- `LoginView` / `RegisterView` - Authentication
- `ScanView` - QR code receipt scanner
- `TransactionsView` - Transaction history
- `ProductsView` - Browse products
- `ProfileView` - User account management
- `FavoriteStoresView` - Manage favorite stores

#### **components/**
- `MainLayout` - App shell with navigation
- `BottomNav` - Mobile navigation bar
- `WebshopModal` - Points redemption modal
- Reusable UI components

#### **stores/**
- `auth.js` - Authentication state (Pinia)
- JWT token management
- User session handling

#### **services/**
- `api.js` - Axios instance with interceptors
- `auth.service.js` - Authentication API calls
- `products.service.js` - Products & stores API
- `transactions.service.js` - Transactions API
- `receipts.service.js` - Receipt scanning
- `reviews.service.js` - Review requests

---

## 📚 API Documentation

### Interactive Documentation

Once the backend is running, access the API documentation:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **Django Admin**: http://localhost:8000/admin/

### Key Endpoints

#### Authentication
```
POST   /api/auth/register/          # Register new user
POST   /api/auth/login/             # Login (get JWT tokens)
POST   /api/auth/refresh/           # Refresh access token
```

#### Products & Stores
```
GET    /api/products/               # List products (paginated)
GET    /api/products/{id}/          # Get product details
GET    /api/products/search/?q=     # Search products

GET    /api/stores/                 # List stores
GET    /api/stores/favorites/       # Get user's favorite stores
POST   /api/stores/favorites/add/   # Add favorite store
DELETE /api/stores/favorites/{id}/  # Remove favorite store
```

#### Receipts & Transactions
```
POST   /api/receipts/scan/          # Scan receipt QR code
GET    /api/transactions/           # List user transactions
GET    /api/transactions/{id}/      # Get transaction details
```

#### Reviews (Unmatched Products)
```
POST   /api/items/{id}/request-review/  # Request admin review
GET    /api/reviews/pending/             # List pending reviews (admin)
POST   /api/reviews/{id}/approve/        # Approve review (admin)
POST   /api/reviews/{id}/reject/         # Reject review (admin)
```

#### Points & Webshop
```
GET    /api/points/balance/         # Get points balance
POST   /api/points/use/             # Use points (webshop)
POST   /api/points/add/             # Add points (webshop)
```

---

## 🎮 Features Guide

### Receipt Scanning

1. Navigate to **Scan Receipt** page
2. Click **Scan QR Code**
3. Point camera at Serbian fiscal receipt QR code
4. System automatically:
   - Fetches receipt details from tax authority
   - Matches products from database
   - Awards points (10 per matched product)
   - Creates transaction record

### Product Review Workflow

1. **User scans receipt** with unmatched products
2. **User requests review** for unmatched items
3. **Admin reviews** in Django admin panel
4. **Admin approves/rejects** the product
5. If approved:
   - Product is created in database
   - Item is linked to product
   - Points are awarded to user
   - Transaction total is updated

### Points System

- **Earn Points**: Scan receipts (10 points per product)
- **View Balance**: Home page displays current points
- **Redeem Points**: Use webshop to purchase rewards
- **Track History**: View all earned/spent points

### Favorite Stores

- Mark frequently visited stores as favorites
- Quick access to favorite store promotions
- Prioritized offers from favorite stores
- Manage favorites from dedicated page

---

## 🔧 Environment Variables

### Backend (.env)

Create `backend/.env` file:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=loyalty_app
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)
```

### Frontend

Frontend environment is configured in `vite.config.js`. API base URL is set to `http://localhost:8000`.

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test

# Run specific test file
python test_api.py
```

### API Testing

Use the provided test script:
```bash
cd backend
python test_api.py
```

Or use the Swagger UI at http://localhost:8000/api/schema/swagger-ui/

### Manual Testing

See `backend/TESTING_GUIDE.md` for detailed testing scenarios.

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist

- [ ] Set `DEBUG=False` in backend/.env
- [ ] Configure proper `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL backup strategy
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up static file serving (Django collectstatic)
- [ ] Configure production CORS settings
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Enable database connection pooling

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8 (Python)
- **Frontend**: Follow Vue.js style guide
- **Commits**: Use conventional commits format

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Serbian Tax Authority API for receipt verification
- Django REST Framework for robust API development
- Vue.js team for excellent frontend framework
- Contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [your-email@example.com]

---

## 🗺️ Roadmap

- [ ] Statistics & Reports dashboard
- [ ] Email notifications for points milestones
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Advanced analytics for admins
- [ ] Integration with more store systems
- [ ] Gamification features (badges, levels)
- [ ] Social sharing capabilities

---

**Built with ❤️ by Viktor Varkulja**
