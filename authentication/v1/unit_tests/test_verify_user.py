import json
from unittest.mock import patch

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

import redis
from authentication.models import Profile
from common import variables
from common.variables import *
from common.utils import (refresh_throttle)
from third_party_repository.ZibalApi import \
    VerificationPhoneNumberWithIdentityCodeResponse

from .base import BaseUserUnitTestCase


class VerifyUserViewSetTests(BaseUserUnitTestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up the necessary data for all test methods in this class.

        This method is called once for the test class and is typically used
        to set up non-modifiable data or configuration that is shared among
        all tests.
        """
        refresh_throttle()

    def setUp(self):
        """
        Prepare the environment for each test case.

        This method is executed before each individual test method and is
        used to set up initial conditions such as creating a test user and
        preparing the data payload for login.
        """
        super().setUp()
        self.url = "http://127.0.0.1:8000/user/v1/api/verify_user/"
        self.confirm_url = 'http://127.0.0.1:8000/user/v1/api/verify_user/confirm_informations/'
        self.client.force_authenticate(
            user=self.user)  # Authenticate as the user

    @patch("third_party_repository.ZibalApi.ZibalService.get_personal_infos")
    @patch("third_party_repository.ZibalApi.ZibalService.verify_phone_number_with_identity_code")
    @patch('authentication.v1.apis.verify_user.VerifyUserViewSet.permission_classes', return_value=[AllowAny])
    def test_verify_user_success(self, mock_permission, mock_zibal_verification_phone, mock_get_personal_info):
        """
        Test successful verification of user information.

        This test verifies the successful verification process of user information
        where the provided data matches the ones returned from the Zibal API.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Mock the `get_personal_infos` method to return user personal information.
        3. Mock the `verify_phone_number_with_identity_code` method to return a successful verification response.
        4. Authenticate the client as a user.
        5. Send a POST request to the verification API endpoint with valid data.
        6. Check that the response status code is 200 OK.
        7. Ensure the response contains user personal information.
        """
        data = {
            variables.PHONE_NUMBER: "9121345675",
            variables.COUNTRY_CODE: "98",
            variables.NATIONAL_CODE: "1234567896",
            variables.BIRTH_DATE: "1381-07-26",
        }
        mock_get_personal_info.return_value = {
            variables.PHONE_NUMBER: "9123456789",
            variables.PERSONAL_INFO: {
                "first_name": "Name",
                "last_name": "Last name"
            },
            variables.COUNT: 1,
            variables.IDENTITY_NUMBER: '1234567890'
        }
        mock_zibal_verification_phone.return_value = VerificationPhoneNumberWithIdentityCodeResponse(
            message='موفق', matched=True, result=1)
        response = self.client.post(self.url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(variables.PERSONAL_INFO, response.data['data'])

    @patch('authentication.v1.apis.verify_user.VerifyUserViewSet.permission_classes', return_value=[AllowAny])
    def test_verify_user_invalid_data(self, mock_permission):
        """
        Test verification with invalid input data.

        This test verifies that the verification process handles invalid input data correctly,
        such as missing required fields.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Send a POST request to the verification API endpoint with invalid data (missing required fields).
        3. Ensure the response status code is 400 Bad Request.
        4. Verify that the response contains the appropriate error message for invalid input data.
        """
        data = {
            # Missing required fields
            variables.COUNTRY_CODE: "98",
            variables.NATIONAL_CODE: "1234567890",
            variables.BIRTH_DATE: "1990-01-01",
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(variables.INVALID_INPUT_DATA, response.data)

    @patch("redis_service.utils.RedisStore.get")
    @patch('authentication.v1.apis.verify_user.VerifyUserViewSet.permission_classes', return_value=[AllowAny])
    def test_verify_user_redis_error(self, mock_permissions, mock_get_from_redis):
        """
        Test verification when Redis connection fails.

        This test verifies that the verification process handles Redis connection failures gracefully.

        Procedure:
        1. Mock the `RedisStore.get` method to raise a `ConnectionError`.
        2. Send a POST request to the verification API endpoint with valid data.
        3. Ensure the response status code is 200 OK.
        4. Verify that the response contains an appropriate error message indicating the Redis connection issue.
        """
        data = {
            variables.PHONE_NUMBER: "9123456789",
            variables.COUNTRY_CODE: "98",
            variables.NATIONAL_CODE: "1234567890",
            variables.BIRTH_DATE: "1990-01-01",
        }
        mock_get_from_redis.side_effect = redis.ConnectionError

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(variables.TRY_AGAIN_LATER, response.data['message'])

    @patch("authentication.v1.serializers.UserVerificationSerializer.get_personal_info")
    @patch('authentication.v1.apis.verify_user.VerifyUserViewSet.permission_classes', return_value=[AllowAny])
    def test_verify_user_too_many_tries(self, mock_permission, mock_get_personal_info):
        """
        Test verification process when the user has made too many attempts.

        This test verifies that the system correctly handles cases where the user
        has exceeded the maximum number of allowed verification attempts.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Mock the `get_personal_info` method to return user personal information with a high attempt count.
        3. Send a POST request to the verification API endpoint with valid data.
        4. Ensure the response status code is 200 OK.
        5. Verify that the response contains an appropriate message indicating too many attempts.
        """
        data = {
            variables.PHONE_NUMBER: "9121345675",
            variables.COUNTRY_CODE: "98",
            variables.NATIONAL_CODE: "1234567896",
            variables.BIRTH_DATE: "1381-07-26",
        }
        mock_get_personal_info.return_value = {
            variables.PHONE_NUMBER: "9123456789",
            variables.PERSONAL_INFO: {
                "first_name": "Name",
                "last_name": "Last name"
            },
            variables.COUNT: 4,
            variables.IDENTITY_NUMBER: '1234567890'
        }

        response = self.client.post(self.url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(variables.USER_TO_MANY_TRY, response.data['message'])



class UpdateUserVerifiedDataTests(BaseUserUnitTestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up the necessary data for all test methods in this class.

        This method is called once for the test class and is typically used
        to set up non-modifiable data or configuration that is shared among
        all tests.
        """
        refresh_throttle()

    def setUp(self):
        """
        Prepare the environment for each test case.

        This method is executed before each individual test method and is
        used to set up initial conditions such as creating a test user and
        preparing the data payload for login.
        """
        super().setUp()
        self.url_confirm = "http://127.0.0.1:8000/user/v1/api/verify_user/confirm_informations/"
        self.user_preview = {
            variables.PERSONAL_INFO: {
                variables.FIRST_NAME: "Name",
                variables.LAST_NAME: "Last name",
            },
            variables.IDENTITY_NUMBER: "1234567896"}

    @patch('authentication.v1.apis.verify_user.UpdateUserVerifiedDataViewSet.permission_classes', return_value=[AllowAny])
    @patch("redis_service.utils.RedisStore.get")
    def test_confirm_informations_success(self, mock_get_preview, mock_permission):
        """
        Test confirming user's information successfully.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Mock the RedisStore get method to return user preview data.
        3. Authenticate the client as a user.
        4. Send a POST request to confirm user information with a valid confirmation token.
        5. Ensure the response status code is 200 OK.
        6. Check that the user's information is updated correctly.
        7. Verify that the response message indicates successful verification.
        """
        self.client.force_authenticate(user=self.user)
        mock_get_preview.return_value = self.user_preview
        response = self.client.post(self.url_confirm, data=json.dumps(
            {CONFIRMATION_TOKEN: str(self.user.pk)}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.get(user=self.user).name,
                         self.user_preview[variables.PERSONAL_INFO][variables.FIRST_NAME])
        self.assertEqual(response.data['message'], USER_VERIFIED_SUCCESSFULLY)

    @patch('authentication.v1.apis.verify_user.UpdateUserVerifiedDataViewSet.permission_classes', return_value=[AllowAny])
    def test_confirm_informations_missing_token(self, mock_permission):
        """
        Test confirming user's information with a missing confirmation token.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Send a POST request to confirm user information without providing a confirmation token.
        3. Ensure the response status code is 400 Bad Request.
        4. Verify that the response contains the message for invalid input data.
        """
        response = self.client.post(self.url_confirm, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, INVALID_INPUT_DATA)

    @patch('authentication.v1.apis.verify_user.UpdateUserVerifiedDataViewSet.permission_classes', return_value=[AllowAny])
    def test_confirm_informations_invalid_token(self, mock_permission):
        """
        Test confirming user's information with an invalid confirmation token.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Send a POST request to confirm user information with an invalid confirmation token.
        3. Ensure the response status code is 400 Bad Request.
        """
        invalid_token = "invalid"

        response = self.client.post(self.url_confirm, data={
                                    CONFIRMATION_TOKEN: invalid_token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('authentication.v1.apis.verify_user.UpdateUserVerifiedDataViewSet.permission_classes', return_value=[AllowAny])
    @patch("redis_service.utils.RedisStore.get")
    def test_confirm_informations_redis_error(self, mock_get_user_preview_data, mock_permission):
        """
        Test confirming user's information when Redis connection fails.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Mock the RedisStore get method to raise a ConnectionError.
        3. Authenticate the client as a user.
        4. Send a POST request to confirm user information.
        5. Ensure the response status code is 200 OK.
        6. Verify that the response contains an appropriate message about the Redis connection error.
        """
        mock_get_user_preview_data.side_effect = redis.ConnectionError
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url_confirm, data={
                                    CONFIRMATION_TOKEN: str(self.user.pk)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], TRY_AGAIN_LATER)
        self.assertEqual(
            response.data['business_status_code'], BUSINESS_STATUS.REDIS_IS_DOWN)

    @patch('authentication.v1.apis.verify_user.UpdateUserVerifiedDataViewSet.permission_classes', return_value=[AllowAny])
    @patch("redis_service.utils.RedisStore.get")
    def test_confirm_informations_user_not_verified(self, mock_get_user_preview_data, mock_permission):
        """
        Test confirming user's information when the user is not verified.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Mock the RedisStore get method to return None, simulating an unverified user.
        3. Authenticate the client as a user.
        4. Send a POST request to confirm user information.
        5. Ensure the response status code is 200 OK.
        6. Verify that the response contains an appropriate message indicating the user is not verified.
        """
        mock_get_user_preview_data.return_value = None  # Simulate user not verified
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url_confirm, data={
                                    CONFIRMATION_TOKEN: str(self.user.pk)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], USER_IS_NOT_VERIFIED)
        self.assertEqual(
            response.data['business_status_code'], BUSINESS_STATUS.USER_IS_NOT_VERIFIED)
