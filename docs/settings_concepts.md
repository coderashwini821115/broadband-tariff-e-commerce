# Django Settings - Key Concepts

## 1. BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

- Defines the **root directory** of the project.
- Built by navigating up from the current settings file using `.parent`.
- Used to build paths relative to the project root, e.g.:
  ```python
  STATIC_ROOT = BASE_DIR / 'staticfiles'
  MEDIA_ROOT = BASE_DIR / 'media'
  TEMPLATES = [{'DIRS': [BASE_DIR / 'templates']}]
  ```

---

## 2. SECRET_KEY

```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')
```

- Used by Django for **cryptographic signing**: session cookies, password reset tokens, CSRF tokens.
- Fetched from environment variables in production.
- The fallback value is only acceptable in development.
- **Never expose or hardcode the secret key in production.**

---

## 3. DEBUG vs Logging Level (Two Different Things)

### `DEBUG = True/False`

Controls Django's behavior at a framework level:

| Feature         | `DEBUG = True`                         | `DEBUG = False`       |
| --------------- | -------------------------------------- | --------------------- |
| Error pages     | Detailed (full stack trace in browser) | Generic 500 page      |
| `ALLOWED_HOSTS` | Not enforced                           | Strictly enforced     |
| Static files    | Served by Django                       | Must use Nginx/Apache |
| SQL query log   | Stored in memory                       | Disabled              |
| Security checks | Relaxed                                | Strict                |

### Logging Level (`LOGGING['loggers']['django']['level']`)

Controls **what gets printed to the terminal**. Completely independent of `DEBUG`:

- `'DEBUG'` → prints everything including autoreload file-watching messages (very noisy).
- `'INFO'` → prints normal server activity only.
- `'WARNING'` → prints only warnings and above.

**Key Point**: `DEBUG = False` does NOT reduce terminal output. You must change the logging level separately.

---

## 4. ALLOWED_HOSTS

```python
ALLOWED_HOSTS = ['*']  # Development only
```

- Controls which hostnames can make requests to the server.
- `'*'` means any host is allowed — only safe in development.
- In production, restrict to your actual domain:
  ```python
  ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
  ```

---

## 5. INSTALLED_APPS

```python
INSTALLED_APPS += ['debug_toolbar']
```

- List of all Django apps loaded for the project.
- In `dev.py`, `debug_toolbar` is added only for development.
- `+=` appends to the base list from `base.py` (DRY principle).

---

## 6. MIDDLEWARE

```python
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
```

- Middleware is code that runs on every request/response cycle.
- Order matters — `.insert(0, ...)` places the debug toolbar middleware **first**.
- Inserted at index 0 so it wraps all other middleware.

---

## 7. EMAIL_BACKEND

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- In development, emails are printed to the console instead of actually sent.
- In production, this is replaced with a real email provider (e.g., Mailgun via django-anymail).

---

## 8. Celery Settings

```python
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True
```

- Celery is a **distributed task queue** for running background/async tasks.
- `CELERY_TASK_ALWAYS_EAGER = True` makes tasks run **synchronously** (no queue) — useful for debugging.
- Redis is used as the **message broker** for Celery:
  ```python
  CELERY_BROKER_URL = 'redis://redis:6379/0'
  ```

---

## 9. REST_FRAMEWORK

```python
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)
```

- Controls how Django REST Framework (DRF) behaves.
- `BrowsableAPIRenderer` adds a **user-friendly HTML interface** for testing APIs in the browser — only added in development.

---

## 10. SIMPLE_JWT (Token Lifetime)

```python
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=24)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)
```

- JWT (JSON Web Tokens) are used for **authentication**.
- `ACCESS_TOKEN_LIFETIME` → how long a user stays logged in before needing to re-authenticate.
- `REFRESH_TOKEN_LIFETIME` → how long a refresh token is valid.
- Lifetime is extended in development to avoid frequent re-logins.

---

## 11. CORS (Cross-Origin Resource Sharing)

```python
CORS_ALLOW_ALL_ORIGINS = True
```

- Controls which external domains can make API requests to your server.
- `True` allows all origins — only safe in development.
- In production, restrict to specific trusted origins:
  ```python
  CORS_ALLOWED_ORIGINS = ['https://yourfrontend.com']
  ```

---

## 12. LOGGING

```python
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'INFO'   # Changed from DEBUG to reduce noise
LOGGING['loggers']['apps']['level'] = 'DEBUG'
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}
```

- `handlers` → where logs are sent (console, file, etc.).
- `loggers` → what component's logs to capture and at what level.
- `django.db.backends` at `DEBUG` → **prints every SQL query** to the console, useful for debugging database issues.
- `propagate: False` → prevents duplicate log entries.

---

## 13. Print Statements in dev.py

```python
print(f"✓ Development settings loaded")
print(f"✓ Database: {DATABASES['default']['NAME']} @ {DATABASES['default']['HOST']}")
print(f"✓ Redis: {CACHES['default']['LOCATION']}")
print(f"✓ Celery Broker: {CELERY_BROKER_URL}")
```

- These execute **when the settings file is first imported** by Django (before the server starts).
- Purpose: quick confirmation that the right settings and services are configured.

---

## 14. Settings File Structure (DRY Principle)

```
config/settings/
├── base.py    ← shared settings for all environments
├── dev.py     ← imports base.py, overrides for development
└── prod.py    ← imports base.py, overrides for production
```

- `from .base import *` in `dev.py` imports all base settings.
- DRY (Don't Repeat Yourself): common settings are written once in `base.py`.
- `DJANGO_SETTINGS_MODULE` environment variable tells Django which file to use.

## ALLOWED_HOSTS and CORS: Key Concepts

### ALLOWED_HOSTS

- **Purpose**: A Django server-side security feature that validates incoming HTTP requests based on the `Host` header.
- **Who Enforces It?**: The Django server itself.
- **Scope**: Ensures that only requests with specific hostnames or IP addresses are processed by the server.
- **Key Points**:
  - Protects against HTTP Host header attacks.
  - Applies to all incoming requests, regardless of their origin.
  - Misconfiguration can lead to security vulnerabilities or rejected requests.

### CORS (Cross-Origin Resource Sharing)

- **Purpose**: A browser-enforced security feature that controls which domains can make cross-origin requests (e.g., AJAX or `fetch` calls) to your server.
- **Who Enforces It?**: The browser.
- **Scope**: Prevents unauthorized JavaScript running in a browser from accessing resources on your server.
- **Key Points**:
  - Protects users from malicious scripts running in their browsers.
  - Only applies to browser-based requests, not direct requests (e.g., via `curl` or Postman).

### Key Differences

| Feature         | `ALLOWED_HOSTS`                     | CORS                                  |
| --------------- | ----------------------------------- | ------------------------------------- |
| **Enforced By** | Django server                       | Browser                               |
| **Purpose**     | Prevents HTTP Host header attacks   | Controls cross-origin requests        |
| **Scope**       | Validates `Host` header in requests | Validates `Origin` header in requests |
| **Impact**      | Affects all incoming requests       | Affects only browser-based requests   |

### Why Both Are Needed

- **`ALLOWED_HOSTS`** protects your **server** from malicious requests with fake `Host` headers.
- **CORS** protects your **users** from malicious cross-origin requests.

### Example Scenarios

1. **If `legit.com` is in `ALLOWED_HOSTS` but not in `CORS_ALLOWED_ORIGINS`**:
   - The server will accept direct requests from `legit.com`.
   - The browser will block cross-origin requests from `legit.com`.
   - This creates a false sense of security, as direct requests (e.g., via `curl`) can still exploit vulnerabilities.

2. **If `legit.com` is in `CORS_ALLOWED_ORIGINS` but not in `ALLOWED_HOSTS`**:
   - The browser will allow cross-origin requests from `legit.com`.
   - The server will reject all requests from `legit.com` due to the `Host` header mismatch.

### Summary

- Use `ALLOWED_HOSTS` to secure your server against unauthorized requests.
- Use CORS to protect your users from malicious cross-origin requests.
- Both are essential for a secure and robust application.

## Docker and Kubernetes Concepts

### 1. Docker: Containerization for Consistency

- **What is Docker?**
  - Docker is a tool that packages an application and its dependencies into a container.
  - Containers ensure that the application runs the same way in development, staging, and production.

- **Key Benefits**:
  - **Consistency**: Eliminates "it works on my machine" issues.
  - **Isolation**: Each container runs in its own environment, preventing conflicts.
  - **Portability**: Containers can run on any machine with Docker installed.

- **Docker in Django Projects**:
  - Use Docker to containerize the Django app, database (e.g., PostgreSQL), and other services (e.g., Redis).
  - Example `docker-compose.yml`:
    ```yaml
    version: "3.8"
    services:
      web:
        build: .
        ports:
          - "8000:8000"
        volumes:
          - .:/code
        depends_on:
          - db
      db:
        image: postgres:13
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
    ```

### 2. Kubernetes: Orchestration for Scaling

- **What is Kubernetes?**
  - Kubernetes (K8s) is a platform for managing and scaling containerized applications.
  - It automates deployment, scaling, and management of containers.

- **Key Features**:
  - **Scaling**: Automatically scale applications based on traffic.
  - **Load Balancing**: Distributes traffic across multiple containers.
  - **Self-Healing**: Restarts failed containers automatically.

- **Kubernetes in Production**:
  - Use Kubernetes to manage Docker containers in production.
  - Define resources like `Deployments`, `Services`, and `Ingress` for your application.
  - Example `deployment.yaml`:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: django-app
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: django
      template:
        metadata:
          labels:
            app: django
        spec:
          containers:
            - name: django
              image: my-django-app:latest
              ports:
                - containerPort: 8000
    ```

### 3. Why Use Docker and Kubernetes Together?

- **Docker** provides consistent environments for your application.
- **Kubernetes** manages and scales those environments in production.
- Together, they:
  - Simplify deployment pipelines.
  - Ensure high availability and fault tolerance.
  - Enable rapid scaling to handle traffic spikes.

### 4. Challenges Without Docker and Kubernetes

- **Manual Setup**: Requires manual installation of dependencies on servers.
- **Inconsistencies**: Development and production environments may differ.
- **Scaling Issues**: Scaling applications horizontally is harder without orchestration.
- **Resource Conflicts**: Services share the same environment, increasing the risk of conflicts.

---

### 5. Dockerfile vs docker-compose.yml — What's the Difference?

| | Analogy | Purpose |
|---|---|---|
| **Dockerfile** | Recipe for a single dish | Builds **one image** — your Django app |
| **docker-compose.yml** | Kitchen coordinator | Runs **multiple containers together** and wires them |

#### Dockerfile = "How to build MY app image"
```dockerfile
FROM python:3.11          # start from this base image
COPY . /app               # copy code into container
RUN pip install -r requirements/dev.txt  # install dependencies
```
Result: a single Docker **image** of your Django app.

#### docker-compose.yml = "Run ALL services together"
Your app needs multiple services running simultaneously. docker-compose.yml defines all of them and handles the networking between them:

```
┌──────────────────────────────────────────────────┐
│               docker-compose.yml                 │
│                                                  │
│  web     → Django (built from your Dockerfile)  │
│  db      → PostgreSQL (official image)           │
│  redis   → Redis (official image)                │
│  celery  → Same Django image, different command  │
└──────────────────────────────────────────────────┘
```

Without docker-compose, you'd have to start each container manually with long `docker run` commands and link them yourself.

---

### 6. How Docker Knows About Environment Variables (The Full Flow)

There are **three layers** — each feeds the next.

#### Layer 1 — `.env` file (secrets, per-developer config)
```
POSTGRES_DB=broadband_platform
POSTGRES_PASSWORD=postgres
ANTHROPIC_API_KEY=sk-ant-xxxx
```

#### Layer 2 — `docker-compose.yml` injects into the container

Two different blocks, two different sources:

```yaml
# Reads ALL variables from .env file and injects into container
env_file:
  - .env

# Hardcodes specific values directly (no .env needed)
environment:
  - DJANGO_SETTINGS_MODULE=config.settings.dev
  - POSTGRES_HOST=db        # "db" = the Docker service name, not a real hostname
  - POSTGRES_PORT=5432
  - REDIS_URL=redis://redis:6379/1
```

**Why split?**
- `.env` → secrets and per-developer values (passwords, API keys)
- `environment:` block → Docker-network-specific values like `POSTGRES_HOST=db` (only meaningful inside Docker)

Both end up in the container's OS environment. Django reads from the same place regardless.

#### Layer 3 — Django `base.py` reads from the container's environment
```python
# base.py line 80-84
DATABASES = {
    'default': {
        'NAME': os.environ.get('POSTGRES_DB', 'broadband_platform'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
```

`os.environ.get('POSTGRES_DB', 'broadband_platform')` means:
- Look for `POSTGRES_DB` in the OS environment
- If not found, use `'broadband_platform'` as the fallback default

#### Complete flow visualized
```
.env file
  └── POSTGRES_DB=broadband_platform
        │
        ▼
docker-compose.yml  (env_file: .env  OR  environment: block)
  └── injects into container's OS environment
        │
        ▼
Django base.py
  └── os.environ.get('POSTGRES_DB') → 'broadband_platform'
        │
        ▼
PostgreSQL connection uses the correct database name
```

#### Rule of thumb
| What | Where to put it |
|------|----------------|
| Secrets (passwords, API keys) | `.env` file via `env_file:` |
| Docker network config (hostnames between services) | `environment:` block directly in compose |
| Never | Hardcoded in Python source code |

---

## AWS Concepts for Backend Development

### 1. Compute Services

#### EC2 (Elastic Compute Cloud):

- Virtual servers in the cloud.
- Use cases:
  - Hosting backend APIs.
  - Running custom applications.
- Key Features:
  - Auto-scaling: Adjusts the number of instances based on traffic.
  - Elastic Load Balancer (ELB): Distributes traffic across multiple EC2 instances.

#### Lambda:

- Serverless compute service.
- Use cases:
  - Microservices.
  - Event-driven applications.
- Key Features:
  - Pay-per-use: Only pay for execution time.
  - No server management.

---

### 2. Storage Services

#### S3 (Simple Storage Service):

- Object storage for files, images, videos, etc.
- Use cases:
  - Storing static assets (e.g., images, CSS, JavaScript).
  - Backups and logs.
- Key Features:
  - Highly durable and scalable.
  - Supports versioning and lifecycle policies.

#### EBS (Elastic Block Store):

- Block storage for EC2 instances.
- Use cases:
  - Persistent storage for databases or applications running on EC2.
- Key Features:
  - Snapshots for backups.
  - High performance for I/O-intensive applications.

#### RDS (Relational Database Service):

- Managed relational databases (e.g., MySQL, PostgreSQL, MariaDB).
- Use cases:
  - Storing structured data for backend applications.
- Key Features:
  - Automated backups and scaling.
  - Multi-AZ (Availability Zone) deployments for high availability.

#### DynamoDB:

- NoSQL database service.
- Use cases:
  - Applications requiring low-latency and high throughput.
  - Storing unstructured or semi-structured data.
- Key Features:
  - Fully managed and serverless.
  - Supports global tables for multi-region replication.

---

### 3. Networking and Content Delivery

#### VPC (Virtual Private Cloud):

- Isolated network for your AWS resources.
- Use cases:
  - Hosting backend services securely.
  - Connecting on-premises data centers to AWS.
- Key Features:
  - Subnets for public and private resources.
  - Security groups and network ACLs for access control.

#### Route 53:

- DNS (Domain Name System) service.
- Use cases:
  - Mapping domain names to backend services.
  - Health checks and failover routing.
- Key Features:
  - Supports routing policies (e.g., latency-based, geolocation).

#### CloudFront:

- Content Delivery Network (CDN).
- Use cases:
  - Caching static assets (e.g., images, CSS, JavaScript).
  - Reducing latency for global users.
- Key Features:
  - Integrated with S3 and Route 53.
  - Supports HTTPS and DDoS protection.

---

### 4. Security and Identity

#### IAM (Identity and Access Management):

- Manages access to AWS resources.
- Use cases:
  - Granting permissions to developers, applications, and services.
- Key Features:
  - Fine-grained access control.
  - Supports roles, policies, and multi-factor authentication (MFA).

#### Secrets Manager:

- Stores and manages sensitive information (e.g., API keys, database credentials).
- Use cases:
  - Securely accessing secrets in backend applications.
- Key Features:
  - Automatic rotation of secrets.
  - Integrated with Lambda and RDS.

#### KMS (Key Management Service):

- Manages encryption keys.
- Use cases:
  - Encrypting data in S3, RDS, or DynamoDB.
- Key Features:
  - Centralized key management.
  - Integrated with AWS services.

---

### 5. Monitoring and Logging

#### CloudWatch:

- Monitoring and observability service.
- Use cases:
  - Tracking application performance.
  - Setting up alarms for resource usage.
- Key Features:
  - Logs, metrics, and dashboards.
  - Integrated with Lambda, EC2, and other services.

#### X-Ray:

- Distributed tracing service.
- Use cases:
  - Debugging microservices and serverless applications.
- Key Features:
  - Visualizes request flows.
  - Identifies bottlenecks and errors.

---

### 6. Application Integration

#### SQS (Simple Queue Service):

- Message queue service.
- Use cases:
  - Decoupling backend components.
  - Handling asynchronous tasks.
- Key Features:
  - Supports standard and FIFO queues.
  - Scales automatically.

#### SNS (Simple Notification Service):

- Pub/Sub messaging service.
- Use cases:
  - Sending notifications to users or services.
  - Triggering Lambda functions.
- Key Features:
  - Supports SMS, email, and HTTP endpoints.
  - Integrated with S3, CloudWatch, and other services.

#### API Gateway:

- Managed service for creating and managing APIs.
- Use cases:
  - Exposing backend services as REST or WebSocket APIs.
- Key Features:
  - Integrated with Lambda and DynamoDB.
  - Supports authentication and rate limiting.

---

### 7. Developer Tools

#### CodePipeline:

- CI/CD service for automating deployments.
- Use cases:
  - Deploying backend applications to EC2, Lambda, or Kubernetes.
- Key Features:
  - Integrates with GitHub, CodeBuild, and CodeDeploy.

#### CodeBuild:

- Builds and tests your code.
- Use cases:
  - Compiling backend code.
  - Running unit tests.
- Key Features:
  - Fully managed and scalable.
  - Supports multiple programming languages.

#### CodeDeploy:

- Automates application deployments.
- Use cases:
  - Deploying updates to EC2, Lambda, or on-premises servers.
- Key Features:
  - Supports blue/green and rolling deployments.

---

### 8. Serverless and Event-Driven Architecture

#### Step Functions:

- Orchestrates workflows using state machines.
- Use cases:
  - Automating backend processes.
  - Coordinating Lambda functions.
- Key Features:
  - Visual workflow editor.
  - Integrated with AWS services.

#### EventBridge:

- Event bus for routing events between services.
- Use cases:
  - Building event-driven architectures.
  - Integrating third-party services with your backend.
- Key Features:
  - Supports custom and SaaS events.
  - Integrated with Lambda, SQS, and Step Functions.

---

### 9. Machine Learning and AI (Optional)

#### SageMaker:

- Managed service for building and deploying machine learning models.
- Use cases:
  - Predictive analytics in backend applications.
- Key Features:
  - Integrated with S3 and Lambda.
  - Supports training, tuning, and deployment.

#### Rekognition:

- Image and video analysis service.
- Use cases:
  - Detecting objects, faces, or text in images.
- Key Features:
  - Integrated with S3 and Lambda.

---

## Django User Model Concepts

### 1. Why CustomUser Instead of Django's Default User?

This is one of the most important architectural decisions in any Django project. Django's built-in `User` model has several limitations that make it unsuitable for production apps.

#### What Django's Default User Looks Like

```python
# Django's built-in User model (simplified)
class User:
    username    # ← login field  (we don't want this)
    email       # ← optional, NOT unique by default
    first_name  # ← split name fields
    last_name
    id          # ← auto-increment integer: 1, 2, 3...
    is_staff    # ← boolean, no proper role system
    is_superuser
```

For a production broadband platform, this has **five real problems**:

---

#### Problem 1 — Login with `username`, not `email`

Every modern app (Netflix, Razorpay, JioFiber) uses **email as the login field**, not username.
With the default User you'd have to work around it everywhere.
With CustomUser you simply declare:

```python
USERNAME_FIELD = 'email'   # email IS the login field now
```

Django's entire auth system (login, JWT token generation, password reset) automatically uses `email` after this one line.

---

#### Problem 2 — `email` is not unique by default

Django's default model allows **two users with the same email** — a bug waiting to happen in production.

```python
# CustomUser enforces uniqueness at the database level
email = models.EmailField(unique=True)
```

---

#### Problem 3 — Integer ID is a security leak

Default `id` is `1, 2, 3...` — which leaks information:
- Attackers can guess the total number of users from their own ID
- URLs like `/api/users/1/` are trivially enumerable

```python
# CustomUser uses UUID — impossible to guess
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# → 550e8400-e29b-41d4-a716-446655440000
```

UUID is the industry standard for production APIs.

---

#### Problem 4 — No proper role system

Default User has `is_staff` and `is_superuser` booleans — not a proper role system.
This platform needs:

```python
class Role(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    ADMIN = 'admin', 'Admin'

role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
```

This enables clean RBAC (Role-Based Access Control) in API permissions.

---

#### Problem 5 — You CANNOT change it after migrations exist

This is the **biggest** reason to use CustomUser from day one.

Django's official docs warn:

> "Changing AUTH_USER_MODEL after you've created database tables is significantly more difficult since it affects foreign keys and many-to-many relationships."

If you start with the default User and later want email login + UUIDs + roles, you'd need to **wipe your entire database and rebuild all migrations**. There is no clean migration path.

**Rule: Always create a CustomUser at the start of every Django project, even if you don't need extra fields yet.**

---

#### Side-by-Side Comparison

| Feature | Default `User` | `CustomUser` |
|---|---|---|
| Login field | `username` | `email` |
| Email unique? | ❌ No | ✅ Yes (DB constraint) |
| Primary key type | Integer (1, 2, 3) | UUID |
| Role system | `is_staff` boolean | `role` field with `TextChoices` |
| Extendable? | Painful after the fact | ✅ Full control from day one |
| Change later? | Database nightmare | Already set up correctly |

---

#### How It's Registered in Settings

```python
# base.py line 94
AUTH_USER_MODEL = 'users.CustomUser'
```

This single line tells Django:
- Use `CustomUser` everywhere the auth system references a user
- All ForeignKey relationships to User automatically point to `CustomUser`
- `get_user_model()` returns `CustomUser` throughout the codebase

Always use `get_user_model()` in your code, never import `CustomUser` directly — it keeps the code decoupled.

```python
# Correct — decoupled
from django.contrib.auth import get_user_model
User = get_user_model()

# Avoid — tightly coupled
from apps.users.models import CustomUser
```

---

## Django Authentication Internals

### 1. Password Hashing — How It Works

You **never hash passwords manually** in Django. You call `user.set_password(raw_password)` and Django handles everything.

#### What `set_password()` does internally

```
user.set_password('mypassword123')
        ↓
Django runs PBKDF2 algorithm:
  - generates a unique random salt
  - runs 600,000 iterations of SHA-256
        ↓
Stores this string in user.password column:
  pbkdf2_sha256$600000$randomSalt$hashedValue==
```

The plain text password `'mypassword123'` is **never stored anywhere**. The DB only ever sees the hash.

#### How login verification works

When a user logs in:
```python
user.check_password('mypassword123')
# → rehashes input using the same salt stored in DB
# → compares result with stored hash
# → True if match, False if not
```

The original password is never recovered — hashing is **one-way**.

#### Why you must NOT hash manually

```python
# NEVER do this
import hashlib
user.password = hashlib.sha256('password').hexdigest()
```

Without a **unique random salt per user**, two users with the same password produce the same hash. An attacker with the hash table can crack all of them at once using a rainbow table.

Django's `set_password()` generates a new random salt for each user — so even two users with identical passwords have completely different hashes in the DB.

---

### 2. `using=self._db` — Multi-Database Support

```python
user.save(using=self._db)
```

Django supports **multiple databases** configured in `settings.py`:

```python
DATABASES = {
    'default': {...},    # main write database
    'replica': {...},    # read-only replica
    'analytics': {...},  # separate analytics database
}
```

`using=` tells Django **which database** to write to.

`self._db` is a property on the Manager that holds the name of the currently configured database. By default it resolves to `'default'`.

#### `user.save()` vs `user.save(using=self._db)`

```python
user.save()                   # always writes to 'default' — hardcoded
user.save(using=self._db)     # writes to whatever DB this manager is configured for
```

If you later call:
```python
User.objects.using('replica').create_user(...)
```

- With `self._db` → correctly saves to `'replica'`
- With plain `save()` → silently ignores and saves to `'default'`

It is a **future-proofing** pattern. Costs nothing now, prevents subtle bugs when read replicas are added in production.

---

### 3. `serializer.save()` vs `user.save()` — The Full Layer Chain

Both `.save()` calls exist, but they operate at **completely different layers** and serve different purposes.

#### The three-layer Django architecture

```
Layer 1 — View (HTTP)
    Receives request, calls serializer

Layer 2 — Serializer (Validation)
    Validates data, calls manager

Layer 3 — Manager (Database)
    Builds user object, hashes password, writes to DB
```

#### The full call chain for user registration

```
POST /api/v1/auth/register/
        ↓
View: serializer.save()        ← triggers the chain
        ↓
Serializer: create(validated_data)
    → calls User.objects.create_user(email, password)
        ↓
Manager: create_user(email, password):
    email = self.normalize_email(email)
    user  = self.model(email=email)   # build object in memory
    user.set_password(password)       # hash password in memory
    user.save(using=self._db)         # ← actual DB INSERT here
        ↓
Row written to PostgreSQL
```

#### Why each layer calls its own save

| Call | Layer | What it does |
|---|---|---|
| `serializer.save()` | Serializer | Triggers `create()` or `update()` on the serializer |
| `serializer.create()` | Serializer | Decides *how* to create — delegates to manager |
| `User.objects.create_user()` | Manager | Handles business logic (normalize, hash) |
| `user.save()` | Model/DB | Executes the SQL INSERT into PostgreSQL |

**Analogy:**
- `serializer.save()` = you hand a filled form to the clerk
- `serializer.create()` = clerk reads the form and decides what to do
- `create_user()` = clerk prepares the file correctly (stamps, signs)
- `user.save()` = clerk files it into the cabinet (actual DB write)

Each layer has one responsibility. The View never touches the DB. The Manager never parses HTTP.

---

### 4. `self.model` in the Manager

```python
user = self.model(email=email, **extra_fields)
```

`self.model` is set automatically by Django — it points to the model class the manager is attached to. Since `CustomUserManager` is assigned to `CustomUser` via `objects = CustomUserManager()`, `self.model` resolves to `CustomUser`.

This means `self.model(email=email)` is equivalent to `CustomUser(email=email)` — but decoupled, so the same manager code works if the model is ever renamed or subclassed.

---

## 15. Docker Cheat Sheet

### Common Lifecycle Commands

| Command | Purpose | When to use |
|---|---|---|
| `docker compose up -d` | Start all services in the background | Daily start of development environment |
| `docker compose up -d --build` | Rebuild images and start | After changing `requirements.txt` or `Dockerfile` |
| `docker compose down` | Stop and remove all containers | End of the day/work session |
| `docker compose ps` | List running containers and their status | To check if everything is healthy |
| `docker compose logs -f web` | Follow (stream) logs for a specific service | To see Django output/errors in real-time |

### Running Commands inside Containers

#### 1. In a Running Container (Recommended)
Use this if the `web` service is already running. It's faster and avoids entrypoint issues.
```powershell
docker exec -it broadband_web python manage.py createsuperuser
```

#### 2. In a New Temporary Container
Use this if the services are stopped or if you need to bypass the default entrypoint.
```powershell
docker compose run --rm --entrypoint "" web python manage.py makemigrations
```
*Note: In PowerShell, use `''` (two single quotes) for the empty entrypoint string.*

### Key Troubleshooting Concepts

- **Volume Mounts (`.:/app`)**: Your local code is synced into the container. Most `.py` changes reflect instantly without a restart.
- **Entrypoint Script**: Runs setup tasks (waiting for DB, running migrations) *before* the main command.
- **Port Mapping (`8000:8000`)**: Maps `localhost:8000` on your Windows machine to port `8000` inside the Linux container.
- **Vmmem / WSL**: The Windows process that manages the Linux VM where Docker runs. Limit its RAM via `.wslconfig` if needed.

---

## 16. DRF Routing: Routers vs. Manual Actions

When working with `ModelViewSet` in Django REST Framework, there are two ways to connect your ViewSet to a URL: Using a **Router**, or manually extracting actions using **`.as_view()`**. Choosing between them depends on whether your URL represents a *Noun* (Resource) or a *Verb* (Action).

### 1. The DefaultRouter (For Nouns / Resources)
The standard way to wire a ViewSet is using a `DefaultRouter`. 

```python
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
```

**What it does:** The router automatically generates 5 standard REST endpoints based on the prefix you give it:
* `GET /users/` $\rightarrow$ `list()`
* `POST /users/` $\rightarrow$ `create()`
* `GET /users/<id>/` $\rightarrow$ `retrieve()`
* `PUT /users/<id>/` $\rightarrow$ `update()`
* `DELETE /users/<id>/` $\rightarrow$ `destroy()`

**When to use it:** Always use Routers when your endpoint represents a Resource (a noun), like `/products/`, `/users/`, or `/subscriptions/`. It is clean, automatic, and enforces strict RESTful standards.

### 2. Manual Action Extraction via `.as_view()` (For Verbs / Actions)
Sometimes, business requirements or frontend teams need a specific URL that is an *Action* (a verb), such as `/register/`, `/login/`, or `/checkout/`.

If you try to use a Router for a verb (`router.register('register', UserViewSet)`), you will accidentally generate nonsensical endpoints like `GET /register/` (to list users) or `DELETE /register/<id>/` (to delete a user).

To prevent this, you manually pluck out **only the specific action you need** and map it to your custom URL:

```python
path('register/', UserViewSet.as_view({'post': 'create'}), name='auth_register')
```

**What it does:** 
1. The dictionary `{'post': 'create'}` translates the incoming HTTP method (`POST`) to the specific Python method inside your ViewSet (`create()`).
2. It completely ignores all other actions (`list`, `destroy`, etc.), keeping the endpoint strictly limited to the one thing it was designed to do.

**When to use it:** Use `.as_view()` when you need to expose a single action from a ViewSet under a highly specific, non-RESTful URL name (like `/register/`).

---

## 17. Authentication: Djoser vs. Custom Implementation

When setting up JWT Authentication in Django, developers typically choose between using a pre-packaged library (like **Djoser**) or building the endpoints manually using **`djangorestframework-simplejwt`**.

### 1. The Djoser Way (Startups & MVPs)
Djoser acts as a massive pre-packaged bundle. By simply adding `path('auth/', include('djoser.urls.jwt'))` to your main `urls.py`, you instantly gain access to a full suite of pre-built endpoints (e.g., `/auth/users/` for registration, `/auth/jwt/create/` for login).

*   **Pros:** Incredible speed. You can set up a full auth system in 5 minutes without writing any Serializers or Views.
*   **Cons:** You are locked into their URL naming conventions and their exact flow. Customizing the registration process (like sending a welcome email or checking an external API) requires overriding their internal classes, which can become messy.

### 2. The Custom Way (Enterprise & Scaling)
In a production-grade or enterprise environment, engineering teams almost always build the auth flow manually using raw tools like `simplejwt`.

*   **Strict API Contracts:** Frontend and mobile teams often require specific, immutable URL names (e.g., `POST /api/v1/auth/register/`). Building custom views allows 100% control over the routing namespace to meet these contracts.
*   **Complex Business Logic:** "Registration" in enterprise apps is rarely just creating a database row. It often involves assigning default plans, triggering celery tasks (like welcome emails), assigning RBAC roles, or syncing with CRMs. Handling this in a custom `RegisterSerializer` keeps the logic clean and isolated.
*   **Security Audits:** Owning the core code for user creation and token generation makes security reviews much more straightforward.

**Summary:** Djoser is excellent for rapid prototyping, but manually wiring your serializers and views is the industry standard for production backends that require deep customization and strict API contracts.

---

## 18. Serializers vs. ModelSerializers

When deciding which base class to use for validation in Django REST Framework, the choice depends entirely on whether you are interacting with a database table.

### `serializers.ModelSerializer`
*   **What it does:** Acts as a shortcut. It inspects a Django database Model and automatically copies its schema (fields like `email`, `phone_number`), preventing you from typing them manually.
*   **When to use:** When you are saving, updating, or listing rows from a database table (e.g., `RegisterSerializer` maps to the `CustomUser` table).

### `serializers.Serializer`
*   **What it does:** Provides a blank canvas. It does not look at the database. You must explicitly define every field (e.g., `refresh = serializers.CharField()`).
*   **When to use:** When you are accepting data from a user that does not map to a database Model. Examples include Search Queries, Password Reset confirmation codes, or Logout tokens.

---

## 19. Overriding Methods and `**kwargs`

When overriding built-in framework methods (like `.save()`), you will often see `**kwargs` (Keyword Arguments) used in the method signature:
`def save(self, **kwargs):`

### Why is this necessary?
When a framework like Django or DRF calls a method internally, it sometimes passes hidden arguments behind the scenes. For example, Django might call `serializer.save(commit=True)` or `serializer.save(update_fields=['email'])`.

If you define your custom method as `def save(self):` without `**kwargs`, the moment Django tries to pass `commit=True`, your application will crash with a `TypeError: save() got an unexpected keyword argument`.

By adding `**kwargs`, you are providing a safety net. You are telling Python: *"I don't care what extra keyword arguments the framework tries to pass to me. Just swallow them up silently in a dictionary so the code doesn't crash."*

---

## 20. JWT Statelessness and Token Blacklisting

JSON Web Tokens (JWTs) are completely **stateless**. The server does not remember you. The math inside the token signature proves you are who you say you are. 

Because of this, you cannot "log out" a user simply by destroying a session on the server (because no session exists).

### How Logout / Blacklisting Works:
To log out, the frontend deletes the short-lived Access Token, and sends the long-lived **Refresh Token** to the backend's `/logout/` endpoint.

When the backend runs `token.blacklist()`:
1. It extracts the unique cryptographic ID of that token (the `jti`).
2. It physically creates a new row in a PostgreSQL database table named `token_blacklist_blacklistedtoken`.
3. From that moment on, whenever anyone tries to use that Refresh Token to get a new Access Token, the server checks the database, sees the ID in the blacklist, and rejects the request.

---

## 21. Database Optimization: Partial Indexing

A standard Database Index (like `db_index=True`) catalogs every single row in a table. In many production scenarios, this is a massive waste of resources.

### What is Partial Indexing?
Partial Indexing allows you to index only a subset of the rows in your table by defining a `condition`. For example:

```python
from django.db.models import Q

class Meta: 
    indexes = [
        models.Index(
            fields=['is_active'],
            condition=Q(is_active=True),
            name='idx_active_plans'
        )
    ]
```

### Why Partial Indexing is Highly Efficient:
*   **Space Efficiency:** Instead of indexing 1,000,000 rows (both active and inactive), if only 10,000 are active, the index is 100x smaller.
*   **Performance:** Smaller indexes easily fit into system memory (RAM). When an API endpoint queries for active records (e.g., `GET /api/v1/plans/`), PostgreSQL can scan this tiny, highly-optimized B-Tree blazingly fast.
*   **Faster Writes:** When inactive records are created or updated, the database completely skips updating this index, saving CPU cycles and disk I/O.

---

## 22. Timestamps: `auto_now_add` vs. `auto_now`

Django provides two convenient arguments for `DateTimeField` to automatically manage object lifecycles without writing manual datetime logic:

### `auto_now_add=True` (Use for `created_at`)
*   **How it works:** It sets the timestamp exactly **once**—the moment the row is first INSERTED into the database.
*   **Behavior:** On any subsequent updates to the row, this field is completely ignored and remains untouched.

### `auto_now=True` (Use for `updated_at`)
*   **How it works:** It sets the timestamp **every single time** the `.save()` method is called on the object.
*   **Behavior:** It intercepts the save operation and silently overwrites the field with the current system time, ensuring you always have a perfect log of the last modification.

---

## 23. Redis Caching, Databases, and Serialization (Pickling)

When you use `django.core.cache`, Django automatically routes data to the caching engine defined in your `settings.py` (e.g., `django-redis`). This keeps your views cleanly decoupled from the actual infrastructure.

### Redis Logical Databases
Redis is not just a single bucket; it has 16 logical databases by default, numbered `0` to `15`.
In a robust Django architecture:
*   **Database `0`:** Typically used by Celery for message brokering and task queues (e.g., `_kombu` keys).
*   **Database `1`:** Configured specifically for Django Caching (`redis://redis:6379/1`). This prevents your application cache from colliding with Celery queues.

### How Data is Stored: Pickling vs. JSON
When Django caches a Python dictionary or QuerySet, it does **not** store it as plain JSON. 
Instead, it uses Python's native **Pickle** module to serialize the data into a binary stream.
*   **Why?** JSON is extremely limited. It cannot serialize complex Python objects like `datetime` fields, sets, or Django Model instances. Pickling allows Django to store *any* Python object exactly as it is.
*   **What it looks like:** In tools like Redis Commander, pickled data appears as "String (Binary)" gibberish mixed with keywords like `builtins.dict`.
*   When `cache.get()` is called, Django pulls the binary blob and instantly un-pickles it back into a flawless Python dictionary.

---

## 24. Cache Invalidation in ViewSets

Cache Invalidation is the process of deleting stale data from the cache so the system is forced to fetch fresh data from the database.

In Django REST Framework's `ModelViewSet`, write operations are mapped to specific methods:
*   `POST` (Create) triggers `perform_create()`
*   `PUT/PATCH` (Update) triggers `perform_update()`
*   `DELETE` (Destroy) triggers `perform_destroy()`

By **overriding** these methods, you can inject cache invalidation logic exactly at the millisecond data changes:

```python
def perform_update(self, serializer):
    # 1. Let the parent class handle the actual database save using super()
    super().perform_update(serializer)
    
    # 2. Instantly wipe the stale Redis cache
    self.clear_cache(serializer.instance)
```

**Understanding `super()`:** 
Using `super()` is crucial. It tells Python to look at the parent class (`ModelViewSet`), find its original method, and execute it. This allows the framework to do the heavy lifting (validation, database writing). Calling `self.perform_update(serializer)` instead would cause infinite recursion and crash the server.

---

## 25. Python Sets and Time Complexity

A **Set** in Python is an unordered collection of unique elements (duplicates are automatically removed). Under the hood, Python Sets are implemented as **Hash Tables**.

### Time Complexity (Big O)
Because they use Hash Tables, Sets are incredibly fast compared to Lists:
*   **Lookup (`x in s`):** $O(1)$ (Instant math). A List is $O(N)$ (requires scanning every item).
*   **Add/Remove:** $O(1)$.

### The $O(N^2)$ Trap
If you have a loop of 10,000 items, and inside that loop you do a lookup `if x in my_list`, the List scan takes up to 10,000 steps per loop. $10,000 \times 10,000 = 100,000,000$ steps ($O(N^2)$).
If you convert the list to a Set first (`my_set = set(my_list)`), the lookup takes 1 step. $10,000 \times 1 = 10,000$ steps ($O(N)$). Always use Sets for lookups inside loops!

### Sets and Caching
JSON cannot serialize Python Sets. This is why Django uses **Pickle** (binary serialization) to store complex data structures in Redis.

---

## 26. Django TextChoices vs. Tuples

Django 3.0 introduced `models.TextChoices` as the modern, Pythonic way to define choices, replacing the legacy list of tuples.

**The Legacy Way:**
```python
ROLE_CHOICES = [('admin', 'Admin'), ('customer', 'Customer')]
# Usage in code: if user.role == 'admin': (Vulnerable to typos like 'avtive')
```

**The Modern Way:**
```python
class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CUSTOMER = 'customer', 'Customer'
# Usage in code: if user.role == User.RoleChoices.ADMIN:
```
*   **Benefits:** IDE Auto-complete, prevention of typo-induced bugs (no "magic strings"), and a single source of truth for the underlying string value.

---

## 27. The N+1 Query Problem in `__str__`

The `__str__` method is evaluated every time an object is printed or displayed, such as in the Django Admin panel. 
If your `__str__` method crosses a foreign key relationship (e.g., `return self.user.email`), it creates a massive performance trap:

*   Loading 50 Subscriptions in the Admin panel triggers 1 query.
*   Evaluating `self.user.email` triggers 50 extra queries (one for each row).
*   Evaluating `self.plan.name` triggers another 50 extra queries.
This results in 101 queries for a single page!

**The Fix:** Use `list_select_related = ['user', 'plan']` in your `admin.py`. This forces Django to perform an **SQL INNER JOIN**, fetching all 50 subscriptions and their related users/plans in exactly 1 single query.

---

## 28. Callables vs. Executing Functions

When passing functions to Django Models or Celery Tasks, the distinction between a Callable and Executing is critical.

### The Callable (No Parentheses): `default=timezone.now`
You are passing the function itself (a "Recipe Card"). You are telling Django: *"Keep this function. Execute it yourself in the future whenever a new database row is inserted."*

### Executing (With Parentheses): `start_date = timezone.now()`
You are actively executing the function right now. If you accidentally use this in a Model definition (`default=timezone.now()`), the function runs exactly once when the server boots up, and every single row created all year will have the exact same timestamp!

---

## 29. Overriding `create()` in ModelSerializers

A standard `Serializer` only converts JSON and validates it. However, a `ModelSerializer` is directly connected to a database table and handles the physical SQL `INSERT`/`UPDATE` operations via its `.save()` method.

When you override `create(self, validated_data)`, you intercept the flow right after validation, but right before the SQL `INSERT`.
```python
def create(self, validated_data):
    # 1. Modify the dictionary (e.g., inject calculated dates)
    validated_data['end_date'] = timezone.now() + timedelta(days=30)
    
    # 2. Hand it back to the parent class to execute the SQL INSERT!
    return super().create(validated_data)
```
If you forget `return super().create(validated_data)` and just return the dictionary, the SQL INSERT never happens, and your database remains empty.

---

## 30. ModelViewSet HTTP Routing and `perform_*` Hooks

Django REST Framework's `ModelViewSet` automatically maps standard HTTP methods to internal Python class methods. 

Here is the exact routing lifecycle when a request hits a `ModelViewSet`:

*   **`GET /api/v1/plans/`** ➡️ `list()` *(Override this to cache the list response)*
*   **`GET /api/v1/plans/<id>/`** ➡️ `retrieve()` *(Override this to cache the detail response)*
*   **`POST /api/v1/plans/`** ➡️ `create()` ➡️ calls `perform_create()`
*   **`PUT/PATCH /api/v1/plans/<id>/`** ➡️ `update()` ➡️ calls `perform_update()`
*   **`DELETE /api/v1/plans/<id>/`** ➡️ `destroy()` ➡️ calls `perform_destroy()`

### Why override `perform_create` instead of `create`?
DRF explicitly splits the writing process into two steps to make your code cleaner:
1.  **`create()`**: Handles the messy HTTP layer (parsing JSON, validating, returning the `201 Created` HTTP response).
2.  **`perform_create()`**: A tiny helper function that solely runs `serializer.save()`.

By overriding `perform_create`, you intercept the process *after* all the HTTP formatting is done but *before* the save happens. This makes it the perfect place to inject context (like the logged-in user) or trigger cache invalidations:

```python
def perform_create(self, serializer):
    # Securely force the subscription to belong to the user making the request
    serializer.save(user=self.request.user)
    
    # Wipe the cache now that data has changed
    self.clear_cache()
```

---

## 31. Attaching Users: ViewSet vs. Serializer Context

When you need to attach the currently logged-in user to a newly created database row (e.g., creating a Subscription), there are two valid architectural approaches in Django REST Framework:

### Approach A: The ViewSet Route (Recommended for Reusability)
You pass the user explicitly in the ViewSet's `perform_create` method:
`serializer.save(user=self.request.user)`
*   **Pros:** Keeps the Serializer completely decoupled from HTTP Requests. If a background Celery worker or terminal script needs to create a Subscription later, it can safely use the `SubscriptionSerializer` without crashing.

### Approach B: The Serializer Context Route
You extract the user from the DRF context directly inside the Serializer's `create` method:
`user = self.context['request'].user`
*   **Pros:** Keeps the ViewSet 100% "thin" (routing only) and pushes all business logic into the Serializer.
*   **Cons:** The Serializer is now strictly dependent on an HTTP Request existing. If called outside of an HTTP request, it will crash with a `KeyError`.

---

## 32. Serializer Overrides: `create()` vs. `save()`

When customizing how data is saved in a `ModelSerializer`, you must decide whether to override `create()` or `save()`.

### When to override `create(self, validated_data)`
*   **Use Case:** Single-table operations where you just need to modify or inject data before it saves.
*   **Why:** `ModelSerializer` has a highly optimized, bug-free internal `create` method. By overriding it, you can tweak the `validated_data` dictionary (e.g., calculating an `end_date`), and then call `return super().create(validated_data)` to let the framework do the heavy lifting of writing the SQL insert.

### When to override `save(self, **kwargs)`
*   **Use Case:** Massive, multi-table transactions (e.g., a Shopping Cart Checkout).
*   **Why:** The default `ModelSerializer.create()` cannot handle creating Orders, mapping multiple CartItems to OrderItems, triggering signals, and managing Database Transactions. For complex, multi-model orchestrations, you must completely bypass the default routing by overriding `def save(self, **kwargs):` and writing the database logic manually.

---

## 33. Restricting ViewSets: Mixins vs. `http_method_names`

If you inherit from `ModelViewSet`, DRF automatically exposes full CRUD operations (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`). To secure an endpoint and remove `PUT/PATCH/DELETE`, you have two architectural choices:

### Approach A: The Mixins Route (The Gold Standard)
Instead of `ModelViewSet`, you inherit from `GenericViewSet` and explicitly add only the mixins you want:
```python
class SubscriptionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
```
*   **Why it's better:** The code for `update()` and `destroy()` physically does not exist in your class. The ViewSet is lighter in memory, and auto-generated API documentation (Swagger/OpenAPI) will be 100% accurate because it can strictly guarantee those endpoints don't exist.

### Approach B: Restricting HTTP Methods
You keep `ModelViewSet` but restrict the allowed methods:
```python
http_method_names = ['get', 'post', 'head', 'options']
```
*   **Why it's used:** It is a quick one-liner. It intercepts disallowed requests and immediately returns a `405 Method Not Allowed` error. However, the update/destroy code remains in memory, and Swagger may occasionally incorrectly document them.

---

## 34. Custom Endpoints: The `@action` Decorator

A `GenericViewSet` paired with a `DefaultRouter` is programmed to strictly understand standard CRUD operations. If you write a custom Python method (e.g., `def cancel(self, request):`), the router will ignore it.

The `@action` decorator is how you communicate with the router to generate a non-standard endpoint:
```python
@action(detail=True, methods=['post'])
def cancel(self, request, pk=None):
```
*   **`detail=True`:** Tells the router this action applies to a *specific* instance. It generates: `/subscriptions/<id>/cancel/`.
*   **`detail=False`:** Tells the router this action applies to the entire collection. It generates: `/subscriptions/cancel/`.

---

## 35. Permissions: Static Attributes vs. Dynamic Methods

Applying permissions in DRF relies heavily on the concept of Callables (Recipe Cards) vs Executing (Baking the Cake):

### 1. Static Attribute (`permission_classes`)
```python
permission_classes = [IsAuthenticated]
```
When defined as a class attribute, you must pass the **Callable Class** (no parentheses). DRF loops through this list on every incoming request and instantiates the classes itself. If you passed `[IsAuthenticated()]`, DRF would attempt to instantiate an already instantiated object, causing a crash.

### 2. Dynamic Method (`get_permissions`)
```python
def get_permissions(self):
    return [IsAuthenticated()]
```
When returning permissions dynamically from a function, you are bypassing DRF's automatic instantiation step. Therefore, you must execute the class yourself (**with parentheses**) and return the fully instantiated object.

---

## 36. Django Threading vs. Synchronous Execution

A common misconception is that because Django uses threads, database operations are non-blocking. This confuses **Thread Context Switching** (OS level) with **Asynchronous Execution** (Code level).

### 1. The Server Level (Concurrent via Threads)
When running Django via Gunicorn, the server spins up multiple worker threads. When User A triggers a database `.save()`, Thread 1 sits idle waiting for PostgreSQL to respond. The Operating System detects this idle state and performs a **Context Switch**, putting Thread 1 to sleep and assigning CPU power to Thread 2 to serve User B. Because of this, the server can handle many concurrent users without freezing.

### 2. The Code Level (Synchronous/Blocking)
However, from the perspective of User A and the specific Python code in Thread 1, `.save()` is strictly **Synchronous (Blocking)**. The Python code completely halts on that line and will not execute the next line of code until PostgreSQL replies. If the database takes 5 seconds, User A's browser will hang for 5 seconds. This is why slow tasks (like sending emails) are offloaded to Celery workers, ensuring the API response returns instantly.

---

## 37. `@staticmethod` and Service Layers

In Python, class methods normally require the `self` parameter so they can access the specific instance of the class. To call a normal method, you must instantiate the class first: `service = PaymentService(); service.create_order()`.

The `@staticmethod` decorator tells Python that the method does NOT need access to `self`. It behaves exactly like a floating function, but it is housed inside a class purely for organizational purposes. This allows you to call the method directly on the class without instantiating it: `PaymentService.create_order()`.

### Why use it in Django?
In Enterprise Django architecture (like the **Service Layer** pattern), we want to keep our `views.py` "skinny" by extracting heavy business logic (like calling the Razorpay API) into a separate `services.py` file. Instead of having hundreds of loose floating functions in that file, we group related functions into classes (like `PaymentService` or `InvoiceService`). Because these functions just process data and don't need to maintain "state" (like a normal object would), we mark them as `@staticmethod`s to make the code cleaner and easier to call.

---

## 38. Idempotency Keys (SHA-256)

**Idempotency** is a mathematical property where an operation can be applied multiple times without changing the result beyond the initial application. In payments, this is a critical safety net.

### The Implementation
We generate a unique hash (SHA-256) based on a combination of stable data:
```python
raw_string = f"{user.id}-{subscription_id}-{today_date}"
idem_key = hashlib.sha256(raw_string.encode()).hexdigest()
```
*   **Why Hashing?** It converts readable data into a fixed-length string that cannot be reversed.
*   **Why the Date?** By including the date, we allow the user to try again tomorrow if their payment fails today, but block them from double-paying on the *same* day.
*   **The Check:** Before calling the Payment Gateway (Razorpay/Stripe), we check if a `Payment` record with this `idempotency_key` already exists in our database. If it does, we simply return the existing order instead of creating a new one.

---

## 39. Locking: Pessimistic vs. Optimistic

When two requests hit the database at the exact same time to modify the same record, we have a **Race Condition**.

### 1. Optimistic Locking
Assumes conflicts are rare. It uses a "version" number.
*   **How it works:** "Update this row ONLY IF the version is still 1."
*   **Outcome:** If someone else updated it first, the second request **crashes** with an error.
*   **Best for:** Wikipedia, Google Docs, Profile updates (Read-heavy, low-stakes).

### 2. Pessimistic Locking (`select_for_update`)
Assumes conflicts will happen and takes them seriously.
*   **How it works:** "Lock this row. Anyone else who tries to read/write it must wait in line until I'm finished."
*   **Outcome:** The second request is **delayed** by a few milliseconds instead of crashing.
*   **Best for:** Payments, Bank Transfers, Inventory management (High-stakes, zero-error tolerance).

### Why Pessimistic is better for Payments
While Optimistic locking technically "works" (it prevents the double-update), it does so by **crashing** the second request with an error. 
1.  **Optimistic:** If two webhooks hit at once, the second one fails with a `500 Server Error`. This triggers the payment gateway (Razorpay) to start a retry cycle, meaning the user's subscription might stay "Pending" for 5 more minutes until the next retry. It also clutters your logs with fake errors.
2.  **Pessimistic:** The second webhook simply pauses for a split second, then completes successfully with a `200 OK`. The user gets an "Active" subscription instantly, and your logs stay clean.


---

## 40. Webhooks and Signature Verification

A **Webhook** is an "Inverse API." Instead of our server calling Razorpay, Razorpay's server calls ours.

### Signature Verification
Because our webhook endpoint is public (unauthenticated), anyone could send a fake POST request to `/webhook/` saying "Payment Successful."
To prevent this, we use **Signature Verification**:
1. Razorpay takes the raw request body and "signs" it using a secret key only we and Razorpay know.
2. They send this signature in the headers (`X-Razorpay-Signature`).
3. Our server re-calculates the signature using our secret and the raw body.
4. If they match, we know the request is 100% authentic.

---

## 41. Distributed Consistency and Retries

In a modern app, your data lives in two places: Your Database and the Payment Gateway's Database. Ensuring they stay in sync is called **Distributed Consistency**.

### What if the Webhook fails?
If our database crashes while processing a success webhook:
1. Our server returns a `500 Server Error` to Razorpay.
2. Razorpay has a built-in **Retry Logic** with exponential backoff.
3. They will automatically try sending the webhook again 5 minutes later, then 30 minutes, then 2 hours.
4. Eventually, when our database is back up, one of these retries will succeed, and the subscription will finally turn `ACTIVE`.

This combination of **Atomic Transactions** (rolling back partial saves) and **Third-Party Retries** ensures that we never lose a payment even during a server crash.

