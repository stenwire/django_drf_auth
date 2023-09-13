import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import CustomUserFactory, TokenFactory

User = get_user_model()


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


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestUserViews:
    def test_register_view(self, api_client):
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_logout_view(self, api_client, logged_in_user, user_token):
        url = reverse("logout")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {user_token['access']}"
        )
        response = api_client.post(
            url, {"refresh": user_token["refresh"]}, format="json"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_token_refresh_view(self, api_client, user_token):
        url = reverse("token-refresh")
        data = {"refresh": user_token["refresh"]}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_login_with_nonexistent_user(self, api_client):
        url = reverse("login")
        data = {"email": "nonexistent@example.com", "password": "testpass123"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_incorrect_password(self, api_client, logged_in_user):
        url = reverse("login")
        data = {
            "email": logged_in_user.email,
            "password": "incorrect_password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_successful_registration(self, api_client):
        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_signup_with_existing_details(self, api_client, logged_in_user):
        url = reverse("register")
        data = {
            "email": logged_in_user.email,
            "username": "newuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_with_non_matching_passwords(self, api_client):
        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password1": "testpass123",
            "password2": "testpass456",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_with_missing_required_fields(self, api_client):
        url = reverse("register")
        data = {"email": "newuser@example.com", "password1": "testpass123"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
