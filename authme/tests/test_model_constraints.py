import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authme.models import CustomUser

from .factories import CustomUserFactory


@pytest.mark.django_db
class TestModelConstraints:
    def test_unique_email(self):
        email = "test@example.com"
        CustomUserFactory(email=email)
        with pytest.raises(IntegrityError) as e:
            user = CustomUserFactory(email=email)
            user.full_clean()
            assert len(str(e.value)) > 1

    def test_unique_username(self):
        username = "user1"
        CustomUserFactory(username=username)
        with pytest.raises(IntegrityError) as e:
            CustomUserFactory(username=username)
            assert len(str(e.value)) > 1
