# Phase 1 Complete - Project Setup Explanation

## 📦 What Was Built

Phase 1 establishes the complete foundation for the Broadband B2C Platform backend. Here's everything that was created and why:

## 🏗️ Core Django Structure

### 1. **Project Configuration (`config/`)**

#### `config/settings/` - Split Settings Architecture
- **`base.py`**: Contains all common settings shared across environments
  - **Why**: Follows DRY principle, centralizes shared configuration
  - **Key Decisions**:
    - UUID primary keys for all models (better for distributed systems)
    - JWT authentication with 1-hour access tokens, 7-day refresh tokens
    - REST Framework with pagination (20 items per page)
    - Comprehensive logging with file rotation (15MB max, 10 backups)
    - Redis cache configured with connection pooling (50 max connections)
    - Custom exception handler for standardized API error responses

- **`dev.py`**: Development-specific settings
  - **Why**: Enables faster development with helpful tools
  - **Key Features**:
    - DEBUG=True for detailed error pages
    - Django Debug Toolbar for SQL query analysis
    - Console email backend (prints emails to terminal)
    - Extended JWT token lifetime (24 hours for convenience)
    - CORS allows all origins
    - Verbose logging including SQL queries

- **`prod.py`**: Production-ready settings
  - **Why**: Security and performance optimizations
  - **Key Features**:
    - DEBUG=False
    - Strict HSTS headers (1 year)
    - Secure cookies (HTTPS only)
    - Database connection pooling (600s timeout)
    - Template caching for faster rendering
    - API rate limiting (100/hour anonymous, 1000/hour authenticated)
    - Only JSON renderer (no browsable API)
    - Error email notifications to admins

#### `config/celery.py` - Async Task Configuration
- **Why**: Handles time-consuming tasks without blocking API requests
- **Beat Schedule Configured**:
  - Renewal reminders at 9 AM daily
  - Subscription expiry check at midnight daily
- **Task Settings**:
  - 30-minute hard time limit
  - 25-minute soft time limit
  - Task tracking enabled for monitoring
  - JSON serialization for compatibility

#### `config/urls.py` - Main URL Routing
- **Why**: Single source of truth for all API endpoints
- **Features**:
  - Swagger UI at `/api/docs/`
  - ReDoc at `/api/redoc/`
  - OpenAPI schema at `/api/schema/`
  - Versioned API endpoints (`/api/v1/`)
  - Debug toolbar only in development

#### WSGI/ASGI Configuration
- **Why**: Standard Django deployment interfaces
- Both use production settings by default

---

## 🐳 Docker Infrastructure

### 1. **Dockerfile** - Production Image
- **Base Image**: `python:3.11-slim`
  - **Why**: Small footprint while including all Python tools
- **Multi-stage considerations**: Single stage for now, can optimize later
- **Security**:
  - Runs as non-root user (`appuser`)
  - No cache directories to reduce image size
- **Health Check**: Ensures container is actually serving requests
- **Default Command**: Gunicorn with 4 workers

### 2. **docker/Dockerfile.dev** - Development Image
- **Why**: Faster iteration during development
- **Differences from production**:
  - Uses Django runserver (auto-reload on code changes)
  - Includes dev tools (ipdb, debug toolbar)
  - No gunicorn needed

### 3. **docker-compose.yml** - Development Stack
- **Services**:
  - **db** (PostgreSQL 15): Primary database
    - Health check ensures DB is ready before app starts
    - Named volume for data persistence
  
  - **redis** (Redis 7): Cache + Celery broker
    - AOF persistence enabled
    - Health check with ping command
  
  - **web** (Django): Main application
    - Volume mount for hot-reload during development
    - Depends on healthy db and redis
    - Exposes port 8000
  
  - **celery**: Async task worker
    - 4 concurrent workers
    - Shares codebase with web service
    - Restarts automatically on failure
  
  - **celery-beat**: Scheduled task runner
    - Uses DatabaseScheduler for dynamic schedules
    - Single instance (prevents duplicate tasks)
  
  - **flower**: Celery monitoring (optional but useful)
    - Web UI at port 5555
    - Real-time task monitoring

- **Networking**: All services on `broadband_network` bridge
  - **Why**: Isolated network, services can communicate by name

- **Volumes**: Persistent storage for:
  - PostgreSQL data
  - Redis data
  - Static files
  - Media uploads

### 4. **docker-compose.prod.yml** - Production Stack
- **Additional Services**:
  - **nginx**: Reverse proxy for serving static files and load balancing
- **Differences**:
  - No volume mounts (code baked into image)
  - Redis password protected
  - Gunicorn instead of runserver
  - Always restart policy
  - No exposed DB/Redis ports (security)

---

## 📋 Requirements Files

### `requirements/base.txt` - Core Dependencies
**Web Framework**:
- `Django==4.2.11`: LTS version, stable and well-supported
- `djangorestframework==3.14.0`: Best REST API framework for Django
- `djangorestframework-simplejwt==5.3.1`: JWT authentication
- `django-filter==23.5`: Query filtering
- `django-cors-headers==4.3.1`: Cross-origin requests

**Database**:
- `psycopg2-binary==2.9.9`: PostgreSQL adapter

**Caching**:
- `redis==5.0.1`: Redis client
- `django-redis==5.4.0`: Django cache backend
- `hiredis==2.3.2`: C parser for Redis (10x faster)

**Async Tasks**:
- `celery==5.3.6`: Distributed task queue
- `celery[redis]`: Redis transport for Celery

**Payments**:
- `razorpay==1.4.1`: Indian payment gateway
- `stripe==8.2.0`: International payment gateway

**AI/LLM**:
- `anthropic==0.18.1`: Claude API client
- `openai==1.12.0`: OpenAI API client

**Communications**:
- `django-anymail[mailgun]==10.2`: Email service abstraction
- `twilio==8.13.0`: SMS service

**Documentation**:
- `drf-spectacular==0.27.1`: OpenAPI 3 schema generation

**Security**:
- `cryptography==42.0.5`: Cryptographic recipes

**Monitoring**:
- `sentry-sdk==1.40.6`: Error tracking

### `requirements/dev.txt` - Development Tools
- **django-debug-toolbar**: SQL query profiling
- **ipython/ipdb**: Enhanced debugging
- **pytest + pytest-django**: Modern testing framework
- **factory-boy + faker**: Test data generation
- **black, flake8, isort, mypy**: Code quality tools
- **pytest-cov**: Code coverage reporting

### `requirements/prod.txt` - Production Extras
- **gunicorn**: WSGI HTTP server (production-grade)
- **gevent**: Async worker type for gunicorn
- **boto3**: AWS SDK (S3, SES, etc.)
- **whitenoise**: Static file serving
- **newrelic**: APM monitoring

---

## 🔐 Environment Configuration

### `.env.example` - Template for Environment Variables
- **Comprehensive**: Includes all possible configuration options
- **Well-documented**: Comments explain each variable
- **Secure defaults**: Uses placeholders, never real secrets
- **Sections**:
  - Django core settings
  - Database configuration
  - Redis/Celery settings
  - Email configuration
  - Payment gateways (Razorpay + Stripe)
  - AI/LLM providers
  - SMS service
  - AWS (S3, SES)
  - Monitoring tools
  - Security settings

**Why this approach**:
- 12-factor app methodology
- Environment-specific configuration
- Secrets never in version control
- Easy to deploy to different environments

---

## 🎯 Django Apps Structure

### 1. **`apps/users/`** - Authentication & User Management
**Fully Implemented** with:
- **Custom User Model** (`CustomUser`):
  - UUID primary key (better for distributed systems)
  - Email-based authentication (more modern than username)
  - Role field (customer/admin) for RBAC
  - Phone number field for SMS notifications
  - Timestamps for audit trail

- **Custom User Manager**:
  - `create_user()`: Handles password hashing
  - `create_superuser()`: Admin creation with proper defaults

- **Serializers**:
  - Registration with password confirmation
  - JWT token with custom claims (includes user role)
  - User profile (read-only and update versions)

- **Views**:
  - Registration endpoint (public)
  - Login with JWT tokens + user data
  - Logout with token blacklisting
  - Current user profile
  - Profile update

- **Permissions** (`permissions.py`):
  - `IsAdmin`: Only admin users
  - `IsCustomer`: Only customer users
  - `IsOwnerOrAdmin`: Resource owner or admin

- **Exception Handler**:
  - Standardized error response format
  - Consistent across all endpoints

### 2-7. **Other Apps** (Skeleton Only)
- Created directory structure
- Apps registered in settings
- URLs configured in main config
- **Why skeleton**: Phase 1 focuses on infrastructure
- Will be implemented in future phases

---

## 🧪 Testing Infrastructure

### `tests/conftest.py` - Pytest Configuration
**Fixtures Provided**:
- `api_client`: DRF test client
- `customer_user`: Test customer
- `admin_user`: Test admin
- `authenticated_client`: Pre-authenticated customer client
- `admin_client`: Pre-authenticated admin client

**Why these fixtures**:
- DRY principle in tests
- Consistent test data
- Easy to write new tests

### `pytest.ini` - Test Configuration
- Auto-discovery of test files
- Coverage reporting (HTML + terminal)
- Coverage threshold: 80% minimum
- Reuses test database for speed
- Custom markers (slow, integration, unit, celery)

---

## 🛠️ Development Tools

### `Makefile` - Common Commands
**Why**: Simplifies repetitive Docker commands
**Commands**:
- `make up`: Start all services
- `make migrate`: Run migrations
- `make test`: Run test suite
- `make coverage`: Generate coverage report
- `make shell`: Django shell
- `make logs`: View logs
- `make clean`: Clean up everything

### `setup.cfg` - Tool Configuration
- **flake8**: Python linter config
- **isort**: Import sorting
- **mypy**: Type checking
- **coverage**: Coverage reporting

### `.gitignore` - Version Control
- Excludes: Python cache, virtual environments, secrets, logs, media files
- **Why**: Keeps repository clean and secure

---

## 🚀 CI/CD Pipeline

### `.github/workflows/ci.yml` - GitHub Actions
**Pipeline Steps**:
1. Checkout code
2. Setup Python 3.11
3. Cache pip packages (faster builds)
4. Install dependencies
5. Run migrations
6. Run tests with coverage
7. Check coverage threshold (80%)

**Why this pipeline**:
- Automated testing on every push
- Catches issues before deployment
- Ensures code quality standards
- PostgreSQL and Redis as services

---

## 🎓 Key Design Decisions & Why

### 1. **Split Settings Architecture**
- **Decision**: Separate base/dev/prod settings
- **Why**: 
  - Different needs per environment
  - Security: production secrets separate
  - Performance: caching/debug settings differ

### 2. **JWT Authentication**
- **Decision**: JWT over session-based auth
- **Why**:
  - Stateless (scales horizontally)
  - Works with mobile apps
  - No session storage needed
  - Standard for modern APIs

### 3. **UUID Primary Keys**
- **Decision**: UUID instead of auto-increment integers
- **Why**:
  - Non-sequential (security)
  - No collisions in distributed systems
  - Can generate client-side
  - Industry standard for modern apps

### 4. **Custom User Model**
- **Decision**: Email-based auth with role field
- **Why**:
  - Email more intuitive than username
  - Role field enables RBAC
  - Easier to extend in future
  - Django best practice (set early)

### 5. **Docker Compose for Development**
- **Decision**: Containerize everything
- **Why**:
  - Consistent environment across team
  - Easy onboarding (just `make up`)
  - Matches production environment
  - Isolates dependencies

### 6. **Celery for Async Tasks**
- **Decision**: Celery + Redis broker
- **Why**:
  - Non-blocking API responses
  - Scheduled tasks (Beat)
  - Scalable (add more workers)
  - Industry standard

### 7. **Redis for Caching**
- **Decision**: Redis for cache + Celery broker
- **Why**:
  - In-memory = fast
  - Doubles as cache and queue
  - Reduces database load
  - TTL support for auto-expiry

### 8. **DRF Spectacular for Docs**
- **Decision**: OpenAPI 3 with Swagger UI
- **Why**:
  - Auto-generated from code
  - Interactive API testing
  - Standard format (OpenAPI)
  - Better than DRF's built-in docs

### 9. **Pytest over unittest**
- **Decision**: Use pytest for testing
- **Why**:
  - More Pythonic syntax
  - Better fixtures
  - Rich plugin ecosystem
  - Faster test discovery

### 10. **Razorpay + Stripe Support**
- **Decision**: Support both payment gateways
- **Why**:
  - Razorpay: Popular in India
  - Stripe: International standard
  - Flexible for different markets
  - Similar integration patterns

---

## 📊 What's Ready to Use

✅ **Complete Django project structure**
✅ **Split settings (dev/prod) with security**
✅ **Docker Compose with all services**
✅ **Users app with JWT authentication**
✅ **RBAC permission system**
✅ **Celery + Celery Beat configured**
✅ **Redis caching setup**
✅ **API documentation (Swagger)**
✅ **Test infrastructure with pytest**
✅ **CI/CD pipeline template**
✅ **Makefile for common tasks**
✅ **Environment configuration**
✅ **Production Docker Compose**

---

## 🎯 Next Steps (Phase 2)

**Phase 2 will implement**:
1. Database migrations for User model
2. User registration API with validation
3. JWT login/logout endpoints
4. Token refresh mechanism
5. RBAC middleware
6. Admin access restrictions
7. Tests for authentication flow
8. Factory fixtures for users

---

## 💡 Learning Points

1. **Settings Split**: Essential for production Django apps
2. **Docker Compose**: Simplifies complex multi-service setups
3. **Custom User Model**: Must be done early, hard to change later
4. **JWT vs Sessions**: JWT better for APIs and mobile
5. **Celery**: Critical for any app with background tasks
6. **Redis**: Versatile - cache, queue, and session store
7. **Environment Variables**: 12-factor app methodology
8. **Testing Setup**: Infrastructure matters as much as tests
9. **CI/CD Early**: Catches issues before they compound
10. **Documentation**: Generated docs save time and stay updated

---

Built by **Ashwini Kumar Pandey**
Learning by building production-grade systems 🚀
