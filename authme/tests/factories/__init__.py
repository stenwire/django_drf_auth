import factory
from pytest_factoryboy import register

from authme.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True


class TokenFactory(factory.Factory):
    class Meta:
        model = dict

    access = factory.Faker("uuid4")
    refresh = factory.Faker("uuid4")
