# Broadband B2C Platform - Backend

Production-grade Django backend for a broadband and energy tariff subscription platform.

## 🚀 Tech Stack

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery 5 with Redis broker
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Payment**: Razorpay / Stripe
- **AI/LLM**: Claude API / OpenAI API
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Testing**: pytest + factory-boy
- **Containerization**: Docker + Docker Compose

## 📋 Features

- ✅ **User Management**: Email-based authentication with JWT tokens, RBAC (customer/admin)
- ✅ **Tariff Plans**: Comprehensive plan management with Redis caching
- ✅ **Subscriptions**: Full subscription lifecycle (create, upgrade, cancel, renew)
- ✅ **Payments**: Razorpay/Stripe integration with webhook handling and idempotency
- ✅ **Billing**: Automated invoice generation with AI-powered summaries
- ✅ **Notifications**: Email and SMS notifications via Celery tasks
- ✅ **AI Features**: Claude API integration for invoice summaries and plan recommendations
- ✅ **Scheduled Tasks**: Celery Beat for renewal reminders and expiry checks

## 🏗️ Project Structure

```
broadband_platform/
├── config/                 # Project settings and configuration
│   ├── settings/
│   │   ├── base.py        # Common settings
│   │   ├── dev.py         # Development settings
│   │   └── prod.py        # Production settings
│   ├── urls.py            # Main URL configuration
│   ├── celery.py          # Celery configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── apps/                   # Django applications
│   ├── users/             # Authentication & user management
│   ├── plans/             # Tariff plan catalogue
│   ├── subscriptions/     # User subscriptions
│   ├── payments/          # Payment gateway integration
│   ├── billing/           # Invoicing & billing history
│   ├── notifications/     # Email & SMS notifications
│   └── ai_features/       # LLM integrations
├── tests/                  # Test suite
├── docker/                 # Docker configurations
├── requirements/           # Python dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Production Dockerfile
├── .env.example           # Environment variables template
└── manage.py              # Django management script
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- PostgreSQL 15 (if not using Docker)
- Redis 7 (if not using Docker)

### Setup with Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd broadband-tariff-e-commerce
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your configuration values.

3. **Build and start services**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - API: http://localhost:8000/api/v1/
   - Admin: http://localhost:8000/admin/
   - API Docs: http://localhost:8000/api/docs/
   - Celery Flower: http://localhost:5555/

### Local Development (Without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements/dev.txt
   ```

3. **Setup PostgreSQL and Redis**
   Ensure PostgreSQL and Redis are running locally.

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Update database and Redis connection details.

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Start Celery worker** (in another terminal)
   ```bash
   celery -A config worker -l info
   ```

9. **Start Celery beat** (in another terminal)
   ```bash
   celery -A config beat -l info
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🧪 Running Tests

### With Docker
```bash
docker-compose exec web pytest
```

### With Coverage
```bash
docker-compose exec web pytest --cov --cov-report=html
```

### Local
```bash
pytest
pytest --cov --cov-report=html
```

## 🔧 Development Commands

### Create Django App
```bash
docker-compose exec web python manage.py startapp app_name apps/app_name
```

### Make Migrations
```bash
docker-compose exec web python manage.py makemigrations
```

### Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Django Shell
```bash
docker-compose exec web python manage.py shell_plus
```

### Database Shell
```bash
docker-compose exec db psql -U postgres -d broadband_platform
```

### Redis CLI
```bash
docker-compose exec redis redis-cli
```

## 📦 Docker Services

The `docker-compose.yml` defines the following services:

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache and Celery broker (port 6379)
- **celery**: Celery worker for async tasks
- **celery-beat**: Celery Beat scheduler for periodic tasks
- **flower**: Celery monitoring tool (port 5555)

## 🔐 Environment Variables

See `.env.example` for all required environment variables. Key variables include:

- `DJANGO_SECRET_KEY`: Django secret key (change in production!)
- `POSTGRES_*`: Database configuration
- `REDIS_URL`: Redis connection URL
- `RAZORPAY_*`: Razorpay payment gateway credentials
- `ANTHROPIC_API_KEY`: Claude API key for AI features
- `EMAIL_*`: Email service configuration
- `TWILIO_*`: SMS service configuration

## 🎯 Development Roadmap

### Phase 1: Project Setup ✅
- Django project structure
- Docker configuration
- Settings split (base/dev/prod)
- Requirements files

### Phase 2: Users App
- Custom User model
- JWT authentication
- RBAC (Role-Based Access Control)

### Phase 3: Plans App
- TariffPlan model and APIs
- Redis caching strategy

### Phase 4: Subscriptions App
- Subscription lifecycle management
- Upgrade/cancel functionality

### Phase 5: Payments App
- Razorpay integration
- Webhook handling
- Idempotency

### Phase 6: Billing App
- Invoice generation
- Celery tasks
- Email notifications

### Phase 7: Celery Beat
- Renewal reminders
- Expiry checker

### Phase 8: AI Features
- Invoice AI summaries
- Plan recommendations

### Phase 9: Tests
- pytest suite
- factory-boy fixtures
- 80%+ coverage

### Phase 10: CI/CD & Docs
- GitHub Actions
- API documentation

## 🤝 Contributing

This is a learning project. Contributions, issues, and feature requests are welcome!

## 📝 License

This project is for educational purposes.

## 👤 Author

**Ashwini Kumar Pandey**

Learning by building production-grade systems.

---

**Current Status**: Phase 1 Complete ✅

Next: Phase 2 - Users App with JWT Authentication and RBAC
