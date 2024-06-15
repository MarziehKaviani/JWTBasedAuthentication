from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class AnonymousTokenPermission(BasePermission):
    def has_permission(self, request, view):
        # TODO Revert This func
        if request.user.is_anonymous:
            anon_token = request.session.get("anon_token")
            if anon_token:
                try:
                    decoded_token = AccessToken(anon_token, verify=False)
                    decoded_token.verify()
                    return True
                except TokenError:
                    return False
            else:
                return False
        else:
            return True
