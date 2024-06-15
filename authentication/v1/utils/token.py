import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from jose import jwt
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from authentication.choices import *
from authentication.models import User
from common.variables import MUST_BE_ANON


def decode_token(token):
    """
    Decode the provided JWT token.

    Parameters:
    ----------
    * `token`: `str`
        The JWT token to be decoded.

    Returns:
    ----------
    `dict`
        A dictionary containing the decoded information from the provided JWT token.

    Notes:
    ----------
    - The function extracts information using the provided JWT token, the signing key, and specified algorithms.
    - `verify_aud` claim is set to `False` to disable audience verification.
    """
    token = str(token).replace('Bearer ', '')
    decoded_token = jwt.decode(
        token,
        settings.SIMPLE_JWT["SIGNING_KEY"],
        algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        options={
            "verify_aud": False,
        },
    )
    return decoded_token


def generate_token(request, user=None):
    """
    Generate authentication token based on user type.

    Parameters:
    ----------
    * `request`: `HttpRequest`
        The Django `HttpRequest` object.
    * `user`: `User`, optional
        User for whom the token needs to be generated.
        Possible values: None for `AnonymousUser`, `User` for regular user.

    Returns:
    ----------
    `dict`
        A dictionary containing the generated authentication token(s).

    Raises:
    ----------
    `ValueError`
        If the `user` is none and the request user is not an instance of `AnonymousUser`.

    Notes:
    ----------
    - For None `user`, an `AccessToken` is generated for an `AnonymousUser`.
    - For other `user` values, a `RefreshToken` and an access token (formatted as Bearer token) are generated for the request user.
    -----
    """

    if not user:
        if not isinstance(request.user, AnonymousUser):
            raise ValueError({"error": MUST_BE_ANON}, status=400)

        anon_token = AccessToken.for_user(request.user)
        request.session["anon_token"] = str(anon_token)
        return {"anon_token": str(anon_token)}
    else:
        if not isinstance(user, User):
            # TODO prevet blocker user from accessing server (https://www.nginx.com/blog/validating-oauth-2-0-access-tokens-nginx/)
            raise ValidationError(
                'The given user should be instanse of User model.', 400)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {"access": f"Bearer {access_token}", "refresh": refresh}
