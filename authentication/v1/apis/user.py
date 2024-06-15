from rest_framework import status, viewsets
from rest_framework.decorators import action

from authentication.models import User
from authentication.v1.serializers import UserSerializer
from common.utils import BaseResponse
from common.variables import *
from common.variables import BUSINESS_STATUS


class UserViewSet(
    viewsets.GenericViewSet,
):
    """
    API endpoint that provides various actions related to User.

    Attributes
    ----------
    * `queryset`: ``QuerySet``
        The set of all User objects.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Get the serializer class for different actions.

        Returns:
        ----------
        ``type``
            Serializer class for the specified action.
        """
        return UserSerializer

    @action(detail=False, methods=[GET])
    def users_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(
            message=None,
            data=serializer.data,
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            business_status_code=BUSINESS_STATUS.SUCCESS)

    @action(detail=True, methods=[GET])
    def user_detail(self, request, pk=None):
        queryset = User.objects.get(pk=pk)
        serializer = self.get_serializer(queryset)
        return BaseResponse(
            message=None,
            data=serializer.data,
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            business_status_code=BUSINESS_STATUS.SUCCESS)
