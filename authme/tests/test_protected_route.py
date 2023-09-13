import pytest
from rest_framework import reverse, status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import CustomUserFactory, TokenFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def logged_in_user():
    user = CustomUserFactory()
    user.set_password("testpass123")
    user.save()
    return user


@pytest.fixture
def user_token(logged_in_user):
    refresh_token = RefreshToken.for_user(logged_in_user)
    return {
        "access": str(refresh_token.access_token),
        "refresh": str(refresh_token),
    }


@pytest.mark.django_db
class TestProtectedRoute:
    def test_access_with_valid_token(self, api_client, user_token):
        url = "http://127.0.0.1:8000/api/v1/greet/"
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {user_token['access']}"
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_access_with_invalid_token(self, api_client):
        url = "http://127.0.0.1:8000/api/v1/greet/"
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
