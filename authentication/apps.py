# authentication/v1/apps.py
from django.apps import AppConfig


class AuthenticationV1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
