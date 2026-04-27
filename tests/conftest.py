"""
Pytest configuration and fixtures.
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """Return DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def customer_user(db):
    """Create a test customer user."""
    return User.objects.create_user(
        email='customer@test.com',
        password='testpass123',
        full_name='Test Customer',
        role='customer'
    )


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    return User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        full_name='Test Admin',
        role='admin',
        is_staff=True
    )


@pytest.fixture
def authenticated_client(api_client, customer_user):
    """Return authenticated API client with customer user."""
    api_client.force_authenticate(user=customer_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return authenticated API client with admin user."""
    api_client.force_authenticate(user=admin_user)
    return api_client
