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
