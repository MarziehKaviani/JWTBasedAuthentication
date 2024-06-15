from datetime import timedelta

from decouple import config

from common.settings import *

# auth tokens
SIMPLE_JWT = {  # TODO fix the time of access token
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=14),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("SECRET_KEY", cast=str),
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "pk",
    "USER_ID_CLAIM": "pk",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

SIMPLE_JWT.update(
    {
        "CLAIMS": {
            "refresh_token": {"type": "string"},
        }
    }
)
