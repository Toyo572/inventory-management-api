# Inventory Management API

A production-ready REST API for inventory management built with Django and Docker. This project demonstrates modern backend development practices including containerization, API design, database management, and CI/CD automation.


[![Docker Build](https://github.com/Toyo572/inventory-management-api/actions/workflows/docker-build.yml/badge.svg)](https://github.com/Toyo572/inventory-management-api/actions)
![Django](https://img.shields.io/badge/django-5.2.7-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## 🎯 Project Overview

A comprehensive inventory management system featuring:
- **RESTful API** with full CRUD operations
- **Stock Management** with real-time tracking
- **Category Organization** for product classification
- **Low Stock Alerts** and reorder level monitoring
- **Interactive API Documentation** with Swagger/ReDoc
- **Dockerized Deployment** with PostgreSQL
- **CI/CD Pipeline** with GitHub Actions

## 🛠️ Tech Stack

- **Framework**: Django 5.2.7 + Django REST Framework 3.16.1
- **Database**: PostgreSQL 16
- **Server**: Gunicorn 23.0.0
- **Containerization**: Docker & Docker Compose
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **CI/CD**: GitHub Actions

## ✨ Features

### Product Management
- Create, read, update, and delete products
- Track SKU, price, stock levels, and status
- Categorize products for better organization
- Advanced filtering and search capabilities

### Stock Tracking
- Record stock movements (in/out/adjustments)
- Real-time inventory updates
- Historical movement logs with notes
- Automated low stock alerts based on reorder levels

### API Documentation
- Interactive Swagger UI at `/api/docs/`
- ReDoc documentation at `/api/redoc/`
- OpenAPI 3.0 schema at `/api/schema/`
- Try all endpoints directly in your browser

## 📋 API Endpoints

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a category
- `GET /api/categories/{id}/` - Retrieve a category
- `PUT /api/categories/{id}/` - Update a category
- `DELETE /api/categories/{id}/` - Delete a category

### Products
- `GET /api/products/` - List all products (with filters)
- `POST /api/products/` - Create a product
- `GET /api/products/{id}/` - Retrieve a product
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `GET /api/products/low-stock/` - List products needing reorder

### Stock Management
- `GET /api/stock-movements/` - List all stock movements
- `POST /api/stock-movements/` - Create a stock movement
- `POST /api/products/{id}/stock-in/` - Add stock to product
- `POST /api/products/{id}/stock-out/` - Remove stock from product

## 🚀 Getting Started

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Toyo572/inventory-management-api.git
cd inventory-management-api
```

2. **Set up environment variables**

Edit `.env` and update with your values:
```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=your-strong-password-here
DB_HOST=db
DB_PORT=5432
```

3. **Build and start the containers**
```bash
docker-compose up --build
```

4. **Run database migrations (in a new terminal)**
```bash
docker-compose exec app python manage.py migrate
```

5. **Create a superuser**
```bash
docker-compose exec app python manage.py createsuperuser
```

6. **Access the application**
- API Docs (Swagger): http://localhost:8000/api/docs/
- API Docs (ReDoc): http://localhost:8000/api/redoc/
- Admin Panel: http://localhost:8000/admin/
- API Base URL: http://localhost:8000/api/

**Default credentials created by entrypoint:**
- Username: `admin`
- Password: `admin123`

## 🐳 Docker Commands

**Start services:**
```bash
docker-compose up
```

**Start in detached mode:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f app
```

**Run migrations:**
```bash
docker-compose exec app python manage.py migrate
```

**Create superuser:**
```bash
docker-compose exec app python manage.py createsuperuser
```

**Access Django shell:**
```bash
docker-compose exec app python manage.py shell
```

**Stop services:**
```bash
docker-compose down
```

**Stop and remove volumes:**
```bash
docker-compose down -v
```

**Rebuild after code changes:**
```bash
docker-compose up --build
```

## 📊 Example API Usage

### Authenticate First
Visit http://localhost:8000/api/docs/ and click the green **"Authorize"** button. Enter your credentials.

### Create a Category
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }'
```

### Create a Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "sku": "ELEC-001",
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with USB receiver",
    "category": 1,
    "price": "29.99",
    "stock_quantity": 100,
    "reorder_level": 20,
    "status": "active"
  }'
```

### Add Stock to Product
```bash
curl -X POST http://localhost:8000/api/products/1/stock-in/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "quantity": 50,
    "notes": "Restocking from supplier ABC"
  }'
```

### Search Products
```bash
curl "http://localhost:8000/api/products/?search=mouse&status=active" \
  -u admin:admin123
```

### Get Low Stock Products
```bash
curl http://localhost:8000/api/products/low-stock/ \
  -u admin:admin123
```

## 🏗️ Project Structure

```
inventory-management-api/
├── .github/
│   └── workflows/
│       └── docker-build.yml        # CI/CD pipeline configuration
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Main settings with DRF & Spectacular
│   ├── urls.py                     # Root URL configuration
│   └── wsgi.py                     # WSGI application entry point
├── elevate/                        # Main Django app
│   ├── migrations/                 # Database migrations
│   ├── __init__.py
│   ├── admin.py                    # Admin panel configuration
│   ├── apps.py
│   ├── models.py                   # Database models (Category, Product, StockMovement)
│   ├── serializers.py              # DRF serializers with validation
│   ├── urls.py                     # App URL patterns
│   └── views.py                    # API views (Class-Based Views)
├── staticfiles/                    # Collected static files (generated)
├── .dockerignore                   # Files excluded from Docker build
├── .env                           # Environment variables (NOT in git)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git exclusions
├── docker-compose.yml             # Multi-container orchestration
├── Dockerfile                     # Docker image definition
├── entrypoint.sh                  # Container startup script
├── manage.py                      # Django management script
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## 🔒 Security Features

- Environment-based configuration (12-factor app methodology)
- Secrets managed through environment variables
- Non-root user in Docker container for security
- PostgreSQL with password authentication
- CSRF protection enabled
- SQL injection protection via Django ORM
- Input validation through DRF serializers
- Authentication required for all endpoints

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Visit http://localhost:8000/api/docs/
2. Click the green **"Authorize"** button
3. Enter credentials: `admin` / `admin123`
4. Click "Authorize" then "Close"
5. Try any endpoint by clicking "Try it out" → "Execute"

### Using Postman
1. Import the OpenAPI schema from http://localhost:8000/api/schema/
2. Set Authorization to "Basic Auth"
3. Enter credentials: `admin` / `admin123`
4. Make requests to any endpoint

### Using curl
All examples above use basic authentication with curl.

## 📈 Advanced Features

### Filtering & Search
```bash
# Filter by category
GET /api/products/?category=1

# Filter by status
GET /api/products/?status=active

# Search by name, SKU, or description
GET /api/products/?search=wireless

# Get products with low stock
GET /api/products/low-stock/

# Combine multiple filters
GET /api/products/?category=1&status=active&search=mouse

# Order results
GET /api/products/?ordering=-created_at
```

### Pagination
All list endpoints support pagination with 20 items per page:
```bash
GET /api/products/?page=1
GET /api/products/?page=2
```

### Stock Movement History
```bash
# Get all movements for a product
GET /api/stock-movements/?product=1

# Filter by movement type
GET /api/stock-movements/?movement_type=in
```

## 🚢 Deployment

### GitHub Container Registry (Automated)
Every push to `main` branch automatically builds and pushes to GitHub Container Registry.

Pull the latest image:
```bash
docker pull ghcr.io/Toyo572/inventory-management-api:latest
```

### Manual Build and Push
```bash
# Build the image
docker build -t inventory-api .

# Tag for your registry
docker tag inventory-api your-registry.com/inventory-api:latest

# Push to registry
docker push your-registry.com/inventory-api:latest
```

## 📝 What This Project Demonstrates

✅ **RESTful API Design** - Proper HTTP methods, status codes, and resource naming  
✅ **Django Best Practices** - Models with relationships, serializers, class-based views  
✅ **Database Design** - Normalized PostgreSQL schema with indexes and constraints  
✅ **Docker Proficiency** - Multi-container setup, health checks, non-root users  
✅ **CI/CD Pipeline** - Automated builds and container registry pushes with GitHub Actions  
✅ **API Documentation** - Interactive OpenAPI/Swagger documentation  
✅ **Production Readiness** - Gunicorn WSGI server, static file handling, environment configs  
✅ **Code Organization** - Clean architecture with separation of concerns  
✅ **Business Logic** - Real-world inventory management with stock tracking  

## 🤝 Contributing

This is a portfolio project. Feedback and suggestions are welcome via issues or pull requests!

## 📄 License

MIT License - Free to use for learning and portfolio purposes.

## 👨‍💻 Author
**Toyosi Ogundele**  
Python Backend Developer


- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/Toyo572)
- LinkedIn: [Your Name](http://linkedin.com/in/toyosiogundele)


---

*Built with Django, Docker, and PostgreSQL* 🚀

## 🆘 Troubleshooting

**Port 8000 already in use:**
```bash
docker-compose down
# On Windows: netstat -ano | findstr :8000
# Kill the process using that port
```

**Database connection refused:**
```bash
# Check database health
docker-compose ps
docker-compose logs db

# Restart database
docker-compose restart db
```

**Migrations not applied:**
```bash
docker-compose exec app python manage.py migrate
```

**Static files not loading:**
```bash
docker-compose exec app python manage.py collectstatic --noinput
docker-compose restart app
```

**Permission denied errors:**
```bash
# Rebuild the image
docker-compose down
docker-compose up --build
```