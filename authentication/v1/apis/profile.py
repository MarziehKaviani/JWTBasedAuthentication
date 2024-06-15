from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import redis
from authentication.models import Profile
from authentication.v1.serializers import (ProfileSerializer)
from common.utils import BaseResponse
from common.validators import check_api_input_data
from common.variables import *
from common.variables import BUSINESS_STATUS


class ProfileViewSet(viewsets.GenericViewSet,):
    """
    API endpoint that allows operations on Profile.

    This viewset provides `list`, `retrieve`, and `show_preview` actions for Profile objects.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=[GET])
    def profiles_list(self, request):
        """
        Retrieve a list of all profiles.

        This action returns a list of all profiles available in the system.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        BaseResponse
            A response object containing the list of profiles, HTTP status code, and business status code.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(
            message=None,
            data=serializer.data,
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            business_status_code=BUSINESS_STATUS.SUCCESS)

    @action(detail=True, methods=[GET])
    def profile_detail(self, request, pk=None):
        """
        Retrieve the details of a specific profile.

        This action returns the details of a profile specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the profile to retrieve.

        Returns
        -------
        BaseResponse
            A response object containing the profile details, HTTP status code, and business status code.
        """
        queryset = Profile.objects.get(pk=pk)
        serializer = self.get_serializer(queryset)
        return BaseResponse(
            message=None,
            data=serializer.data,
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            business_status_code=BUSINESS_STATUS.SUCCESS)

