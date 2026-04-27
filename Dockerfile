# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements/ /app/requirements/

# Install Python dependencies
ARG ENVIRONMENT=dev
RUN if [ "$ENVIRONMENT" = "prod" ]; then \
        pip install --upgrade pip && pip install -r requirements/prod.txt; \
    else \
        pip install --upgrade pip && pip install -r requirements/dev.txt; \
    fi

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Create a non-root user to run the app
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/admin/login/?next=/admin/')"

# Default command
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
