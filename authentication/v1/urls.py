from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication.permissions import AnonymousTokenPermission
from authentication.v1.apis.country import PhoneNumberCountryViewSet
from authentication.v1.apis.login import (AnonymousUserViewSet, LoginViewSet,
                                          TokenRefreshWithPermission,
                                          VerificationCodeViewSet)
from authentication.v1.apis.profile import (ProfileViewSet)
from authentication.v1.apis.user import UserViewSet
from authentication.v1.apis.verify_user import VerifyUserViewSet, UpdateUserVerifiedDataViewSet

# TODO Check Path
router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"", LoginViewSet, basename="login")
router.register(r"anonymous_user", AnonymousUserViewSet,
                basename="anonymous_user")
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'', VerifyUserViewSet, basename='verify_user')
router.register(r'verification_code', VerificationCodeViewSet,
                basename='verification_code')
router.register(r'verify_user', UpdateUserVerifiedDataViewSet,
                basename='confirm_user_data')

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/token/refresh/",
        TokenRefreshWithPermission.as_view(
            permission_classes=[AnonymousTokenPermission]
        ),
        name="token_refresh",
    ),
    path('api/countries/', PhoneNumberCountryViewSet.as_view(), name='country-list'),
]
