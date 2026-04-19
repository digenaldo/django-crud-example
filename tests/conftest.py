"""
Shared pytest fixtures for the test suite.
"""
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import django
from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings


@pytest.fixture(scope='session')
def django_setup():
    """Set up Django for testing."""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conceptu.settings')
        django.setup()


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_directory = tempfile.mkdtemp()
    yield Path(temp_directory)
    shutil.rmtree(temp_directory)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file for testing."""
    temp_file_path = temp_dir / "test_file.txt"
    temp_file_path.write_text("test content")
    return temp_file_path


@pytest.fixture
def mock_settings():
    """Mock Django settings for testing."""
    return Mock()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        'name': 'Test Product',
        'description': 'A test product description',
        'price': 29.99,
        'category': 'Test Category'
    }


@pytest.fixture
def mock_request():
    """Mock HTTP request object."""
    request = Mock()
    request.method = 'GET'
    request.GET = {}
    request.POST = {}
    request.user = Mock()
    request.user.is_authenticated = False
    return request


@pytest.fixture
def authenticated_request(mock_request, sample_user_data):
    """Mock authenticated HTTP request."""
    mock_request.user.is_authenticated = True
    mock_request.user.username = sample_user_data['username']
    mock_request.user.email = sample_user_data['email']
    return mock_request


@pytest.fixture
def mock_database():
    """Mock database operations."""
    with patch('django.db.models.Model.save') as mock_save, \
         patch('django.db.models.Model.delete') as mock_delete:
        yield {
            'save': mock_save,
            'delete': mock_delete
        }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Grants database access to all tests.
    This fixture runs automatically for all tests.
    """
    pass


@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return _create_user


@pytest.fixture
def admin_user(user_factory):
    """Create an admin user for testing."""
    return user_factory(
        username='admin',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def logged_in_client(client, user_factory):
    """Client with logged in user."""
    user = user_factory()
    client.force_login(user)
    return client, user


@pytest.fixture(scope='function')
def isolated_media_root(settings, temp_dir):
    """Isolate media files for testing."""
    original_media_root = settings.MEDIA_ROOT
    settings.MEDIA_ROOT = str(temp_dir / 'media')
    yield settings.MEDIA_ROOT
    settings.MEDIA_ROOT = original_media_root