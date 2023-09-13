from pytest_factoryboy import register

from .factories import CustomUserFactory, TokenFactory

register(CustomUserFactory)
register(TokenFactory)
