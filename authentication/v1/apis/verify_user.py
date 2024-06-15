from decouple import config
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

import redis
from authentication.models import Profile
from authentication.v1.serializers import UserVerificationSerializer, PersonalInfoConfirmationSerializer
from authentication.v1.utils.utils import normilize_phone_number
from authentication.validators import (PhoneNumberValidatorAdapter,
                                       country_code_validator,
                                       national_code_validator)
from common import variables
from common.utils import BaseResponse
from common.validators import check_api_input_data
from common.variables import *
from common.utils import countries_hints_dict
from redis_service.utils import RedisStore
from third_party_repository.ZibalApi import ZibalService


def normalize_birth_date(date):
    return str(date).replace('-', '/').strip()


class VerifyUserViewSet(viewsets.GenericViewSet):
    """
    ViewSet for verifying user information.
    """
    queryset = Profile.objects.all()
    serializer_class = UserVerificationSerializer

    @action(methods=['post'], detail=False)
    def verify_user(self, request):
        """
        Verify user information.

        This endpoint validates and verifies user information, including phone number,
        country code, national code, and birth date. It checks if the user's phone number
        matches the provided personal information.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object containing user information.

        Returns
        -------
        Response
            A response indicating the success or failure of the verification process.
        """

        # Check input data
        required_fields = [variables.NATIONAL_CODE, variables.BIRTH_DATE,
                           variables.PHONE_NUMBER, variables.COUNTRY_CODE]
        if not check_api_input_data(request, required_fields):
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Validate Input data
        phone_number = request.data.get(variables.PHONE_NUMBER)
        country_code = request.data.get(variables.COUNTRY_CODE)
        # TODO add validator for this too
        birth_date = request.data.get(variables.BIRTH_DATE)
        national_code = request.data.get(variables.NATIONAL_CODE)

        if not national_code_validator(national_code):
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        if not country_code_validator(country_code):
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        if not PhoneNumberValidatorAdapter(phone_number, country_code).validate():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                exception=True,
                data={
                    "message": f"{variables.INVALID_PHONE_NUMBER}. The supported formet for selected country is: {countries_hints_dict[country_code]}"
                }
            )
        normalized_phone_number = normilize_phone_number(
            phone_number, country_code)
        validated_data = {
            variables.PHONE_NUMBER: normalized_phone_number,
            variables.COUNTRY_CODE: country_code,
            variables.NATIONAL_CODE: national_code,
            variables.BIRTH_DATE: birth_date,
        }
        normalized_birth_date = normalize_birth_date(birth_date)

        # Send data to serializer
        serializer = UserVerificationSerializer(data=validated_data)
        if not serializer.is_valid():
            return BaseResponse(
                message=variables.INVALID_INPUT_DATA,
                data=serializer.errors,
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.INVALID_INPUT_DATA,
                is_exception=True)

        # verify user
        try:
            personal_info = serializer.get_personal_info(request.user)
        except redis.ConnectionError:
            # TODO add this to a log server
            return BaseResponse(
                data=None,
                message=variables.TRY_AGAIN_LATER,
                is_exception=True,
                business_status_code=BUSINESS_STATUS.REDIS_IS_DOWN,
                http_status_code=status.HTTP_200_OK
            )
        if personal_info and request.user.phone_number == personal_info[variables.PHONE_NUMBER]:
            print(personal_info, 22222222222222)
            return BaseResponse(
                message=None,
                data=personal_info[variables.PERSONAL_INFO],
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.SUCCESS,
                is_exception=True)
        else:
            count = int(personal_info[variables.COUNT]
                        ) + 1 if personal_info else 0
            if count > 3:
                return BaseResponse(
                    message=variables.USER_TO_MANY_TRY,
                    data=None,
                    http_status_code=status.HTTP_200_OK,
                    business_status_code=BUSINESS_STATUS.USER_DONT_HAVE_ACCESS,
                    is_exception=True
                )
            zibal_token = config(variables.ZIBAL_TOKEN, cast=str)
            zibal_service = ZibalService(token=zibal_token)
            result = zibal_service.verify_phone_number_with_identity_code(
                phone_number=normalized_phone_number,
                identity_code=national_code,
            )
            if not result:
                return BaseResponse(
                    http_status_code=status.HTTP_200_OK,
                    business_status_code=BUSINESS_STATUS.INVALID_USER_DATA,
                    data=None,
                    message=variables.INVALID_USER_INFO,
                    is_exception=False
                ) 
            if result.matched:
                personal_info = zibal_service.get_personal_infos(
                    identity_code=national_code, birth_date=normalized_birth_date)
                print(personal_info, 111111111111111111111)
                if not personal_info:
                    return BaseResponse(
                        http_status_code=status.HTTP_200_OK,
                        business_status_code=BUSINESS_STATUS.USER_INFO_NOT_MATCHED,
                        data=None,
                        message=variables.USER_INFO_NOT_MATCHED,
                        is_exception=False
                    )
                try:
                    serializer.add_preview_to_redis(
                        personal_info, request.user, count, national_code)
                except redis.ConnectionError:
                    # TODO add this to a log server
                    return BaseResponse(
                        data=None,
                        message=variables.TRY_AGAIN_LATER,
                        is_exception=True,
                        business_status_code=BUSINESS_STATUS.REDIS_IS_DOWN,
                        http_status_code=status.HTTP_200_OK
                    )
                return BaseResponse(
                    message=None,
                    data=personal_info,
                    http_status_code=status.HTTP_200_OK,
                    business_status_code=BUSINESS_STATUS.SUCCESS,
                    is_exception=False)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserVerifiedDataViewSet(viewsets.GenericViewSet):
    """
    API endpoint for updating user verified data.

    This viewset provides an action to confirm user information.
    """
    queryset = Profile.objects.all()
    serializer_class = PersonalInfoConfirmationSerializer

    @action(detail=False, methods=[GET])
    def show_preview(self, request):
        """
        Show a preview of the user's profile.

        This action returns a preview of the profile for the current user.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        BaseResponse
            A response object containing the profile preview, HTTP status code, and business status code.
        """
        try:
            preview = self.get_serializer_class()().show_preview(request.user)
        except redis.ConnectionError:
            # TODO add this to a log server
            return BaseResponse(
                data=None,
                message=TRY_AGAIN_LATER,
                is_exception=True,
                business_status_code=BUSINESS_STATUS.REDIS_IS_DOWN,
                http_status_code=status.HTTP_200_OK
            )
        if preview:
            print(preview)
            return BaseResponse(
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.SUCCESS,
                message=None,
                data=preview,
                is_exception=False
            )
        else:
            return BaseResponse(
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.USER_IS_NOT_VERIFIED,
                message=USER_IS_NOT_VERIFIED,
                data=None,
                is_exception=True)

    @action(detail=False, methods=[POST])
    def confirm_informations(self, request):
        """
        Confirm user's information.

        This action confirms the user's information using a confirmation token and updates the profile accordingly.
        The token is user primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object containing the confirmation token.

        Returns
        -------
        BaseResponse or Response
            A response object indicating the success or failure of the confirmation process.
        """
        # Check input data
        required_fields = [CONFIRMATION_TOKEN]
        if not check_api_input_data(request, required_fields):
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=INVALID_INPUT_DATA)

        # Validate Input data
        confirmation_token = request.data.get(CONFIRMATION_TOKEN)

        # Send data to serializer
        serializer = self.get_serializer_class()(
            data={CONFIRMATION_TOKEN: confirmation_token})
        if not serializer.is_valid():
            return BaseResponse(
                message=INVALID_INPUT_DATA,
                data=serializer.errors,
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.INVALID_INPUT_DATA,
                is_exception=True
            )
        if str(request.user.pk) != str(confirmation_token).strip():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user_preview = serializer.get_user_preview_data(request.user)
        except redis.ConnectionError:
            # TODO add this to a log server
            return BaseResponse(
                data=None,
                message=TRY_AGAIN_LATER,
                is_exception=True,
                business_status_code=BUSINESS_STATUS.REDIS_IS_DOWN,
                http_status_code=status.HTTP_200_OK
            )
        if not user_preview:
            return BaseResponse(
                http_status_code=status.HTTP_200_OK,
                business_status_code=BUSINESS_STATUS.USER_IS_NOT_VERIFIED,
                message=USER_IS_NOT_VERIFIED,
                data=None,
                is_exception=True)

        serializer.update_profile(request.user, user_preview)

        return BaseResponse(
            http_status_code=status.HTTP_200_OK,
            business_status_code=BUSINESS_STATUS.SUCCESS,
            message=USER_VERIFIED_SUCCESSFULLY,
            data=None,
            is_exception=True
        )
