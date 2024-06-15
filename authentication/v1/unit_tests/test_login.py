import json
from unittest.mock import MagicMock, patch

from rest_framework import status

import redis
from authentication.v1.apis import *
from authentication.v1.serializers import *
from common.utils import BaseTime, authenticate_user, refresh_throttle
from common.variables import *
from common.utils import countries_hints_dict

from .base import BaseUserUnitTestCase


class UnitTestLoginView(BaseUserUnitTestCase):

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
        self.phone_number = '9121234567'
        self.country_code = '98'
        self.url = "http://127.0.0.1:8000/user/v1/api/login/"

        self.phone_number = "9131234567"
        self.country_code = "98"
        self.verification_code = "123456"

        self.user = User.objects.create(
            phone_number=f"00{self.country_code}{self.phone_number}", state=variables.PENDING)
        self.valid_payload = {
            variables.PHONE_NUMBER: self.phone_number,
            variables.COUNTRY_CODE: self.country_code,
            variables.VERIFICATION_CODE: self.verification_code
        }

    @patch("authentication.v1.serializers.LoginSerializer.get_original_otp")
    def test_login_success(self, mock_get_original_otp,):
        """
        Test successful login with valid phone number and verification code.

        This test verifies the successful login process where the provided phone 
        number and verification code match the ones stored in the system.

        Procedure:
        1. Mock the `get_original_otp` method to return a valid verification code and expiration time.
        2. Send a POST request to the login API endpoint with the valid payload.
        3. Check that the response status code is 200 OK.
        4. Ensure the response contains access and refresh tokens.
        5. Verify that the response message indicates the user has logged in successfully.
        """
        mock_get_original_otp.return_value = {
            variables.VERIFICATION_CODE: self.verification_code,
            variables.EXPIRTION_TIME: BaseTime().timedelta(minutes=5),
        }
        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(variables.ACCESS_TOKEN, response.data['data'])
        self.assertIn(variables.REFRESH_TOKEN, response.data['data'])
        self.assertEqual(response.data['message'], variables.USER_LOGGED_IN)

    def test_login_without_any_verification_code_in_redis(self):
        """
        Test the login process when no verification code is found in Redis.

        This test checks the scenario where a user attempts to log in without having 
        requested a verification code first. Since there is no code stored in Redis,
        the system should return an invalid OTP response.

        Procedure:
        1. Construct the data payload with the phone number, country code, and a 
           verification code that was not stored in Redis.
        2. Send a POST request to the login API endpoint with the data payload.
        3. Verify that the response status code is 200 OK.
        4. Check that the response message indicates an invalid OTP.
        5. Confirm that the business status code reflects an invalid login credential.
        """
        data = {variables.PHONE_NUMBER: self.phone_number,
                variables.VERIFICATION_CODE: 123456, variables.COUNTRY_CODE: self.country_code}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[variables.MESSAGE], variables.INVALID_OTP)
        self.assertEqual(response.data['business_status_code'],
                         variables.BUSINESS_STATUS.INVALID_LOGIN_CREDENTIONAL)

    @patch("authentication.v1.serializers.LoginSerializer.get_original_otp")
    def test_login_invalid_otp(self, mock_get_original_otp):
        """
        Test login failure due to invalid OTP.

        This test examines the scenario where the user provides an invalid OTP during 
        the login attempt. Even though the phone number is valid, the incorrect OTP 
        should cause the login to fail.

        Procedure:
        1. Mock the `get_original_otp` method to return a valid verification code.
        2. Modify the valid payload to include an incorrect verification code.
        3. Send a POST request to the login API endpoint with the modified payload.
        4. Verify that the response status code is 200 OK.
        5. Check that the response message indicates an invalid OTP.
        6. Confirm that the business status code reflects invalid login credentials.
        """
        mock_get_original_otp.return_value = {
            # here is the valid verification code
            variables.VERIFICATION_CODE: self.verification_code,
            variables.EXPIRTION_TIME: BaseTime().timedelta(minutes=5),
        }
        invalid_verification_code = "654321"
        self.valid_payload[variables.VERIFICATION_CODE] = invalid_verification_code
        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], variables.INVALID_OTP)
        self.assertEqual(response.data['business_status_code'],
                         variables.BUSINESS_STATUS.INVALID_LOGIN_CREDENTIONAL)

        """
        Test login failure due to missing required fields.

        This test checks the response of the login API when the required fields 
        are missing from the payload. The absence of critical data should trigger 
        a validation error.

        Procedure:
        1. Create an invalid payload that omits required fields.
        2. Send a POST request to the login API endpoint with the invalid payload.
        3. Verify that the response status code is 400 BAD REQUEST.
        4. Check that the response indicates invalid input data.
        """
        invalid_payload = {
            variables.PHONE_NUMBER: self.phone_number,
        }
        response = self.client.post(self.url, data=json.dumps(
            invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, variables.INVALID_INPUT_DATA)

    def test_login_user_does_not_exist(self,):
        """
        Test login failure when the user does not exist.

        This test covers the scenario where a login attempt is made with a phone 
        number that does not correspond to any existing user in the system.

        Procedure:
        1. Change the valid payload to include a non-existing phone number.
        2. Send a POST request to the login API endpoint with this payload.
        3. Verify that the response status code is 200 OK.
        4. Check that the response message indicates the user does not exist.
        5. Confirm that the business status code reflects the user was not found.
        """
        non_existing_phone_number = "9112345678"
        self.valid_payload[variables.PHONE_NUMBER] = non_existing_phone_number

        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         variables.USER_DOSE_NOT_EXISTS)
        self.assertEqual(
            response.data['business_status_code'], variables.BUSINESS_STATUS.USER_NOT_FOUND)

    @patch("authentication.v1.serializers.LoginSerializer.get_original_otp")
    def test_login_with_expired_otp(self, mock_get_original_otp):
        """
        Test login failure due to expired OTP.

        This test examines the scenario where the user attempts to log in with an OTP 
        that has expired. The system should reject the login attempt with an invalid OTP response.

        Procedure:
        1. Mock the `get_original_otp` method to return a verification code that has expired.
        2. Send a POST request to the login API endpoint with the valid payload.
        3. Verify that the response status code is 200 OK.
        4. Check that the response message indicates an invalid OTP due to expiration.
        5. Confirm that the business status code reflects invalid login credentials.
        """
        mock_get_original_otp.return_value = {
            variables.VERIFICATION_CODE: self.verification_code,
            variables.EXPIRTION_TIME: BaseTime.now() - BaseTime.timedelta(minutes=1),
        }
        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], variables.INVALID_OTP)
        self.assertEqual(response.data['business_status_code'],
                         variables.BUSINESS_STATUS.INVALID_LOGIN_CREDENTIONAL)

    def test_login_with_invalid_phone_number_format(self):
        """
        Test login failure due to invalid phone number format.

        This test checks the response of the login API when the provided phone number
        does not match the expected format for the selected country code. The system 
        should reject the login attempt and return an error message specifying the 
        valid phone number format.

        Procedure:
        1. Construct an invalid payload with an incorrect phone number format.
        2. Send a POST request to the login API endpoint with the invalid payload.
        3. Verify that the response status code is 400 BAD REQUEST.
        4. Check that the response message indicates the phone number format is invalid.
        5. Ensure the response specifies the expected phone number format for the given country code.
        """
        invalid_payload = {
            variables.PHONE_NUMBER: "invalid_phone_number",
            variables.COUNTRY_CODE: self.country_code,
            variables.VERIFICATION_CODE: self.verification_code
        }
        response = self.client.post(self.url, data=json.dumps(
            invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], f"{INVALID_PHONE_NUMBER}. The supported formet for selected country is: {countries_hints_dict[self.country_code]}")

    def test_login_with_blocked_user(self):
        """
        Test login failure when the user is blocked or suspended.

        This test verifies the system's response when a blocked or suspended user attempts
        to log in. The system should prevent the login and return an appropriate error message
        indicating that the user is blocked.

        Procedure:
        1. Block the user account in the setup method.
        2. Send a POST request to the login API endpoint with the valid payload.
        3. Verify that the response status code is 200 OK.
        4. Check that the response message indicates the user is blocked.
        5. Confirm that the business status code reflects the user is blocked.
        """
        self.user.block()
        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], variables.BLOCKED_USER)
        self.assertEqual(
            response.data['business_status_code'], variables.BUSINESS_STATUS.USER_IS_BLOCKED)

    @patch("authentication.v1.serializers.LoginSerializer.get_original_otp")
    @patch("redis_service.utils.RedisStore.get")
    def test_login_when_redis_is_down(self, mock_get_original_otp, mock_redis_get):
        """
        Test login failure when Redis service is down.

        This test checks the system's behavior when the Redis service, which is 
        used to store and retrieve verification codes, is unavailable. The system 
        should handle the Redis connection error gracefully and return a message
        indicating the user should try again later.

        Procedure:
        1. Mock the Redis `get` method to simulate a Redis connection error.
        2. Mock the `get_original_otp` method to return a valid verification code and expiration time.
        3. Send a POST request to the login API endpoint with the valid payload.
        4. Verify that the response status code is 200 OK.
        5. Check that the response message indicates a retry is necessary due to system issues.
        6. Confirm that the business status code reflects the Redis service is down.
        """
        mock_redis_get.side_effect = redis.ConnectionError
        mock_get_original_otp.return_value = {
            variables.VERIFICATION_CODE: self.verification_code,
            variables.EXPIRTION_TIME: BaseTime().timedelta(minutes=5),
        }
        response = self.client.post(self.url, data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], variables.TRY_AGAIN_LATER)
        self.assertEqual(
            response.data['business_status_code'], variables.BUSINESS_STATUS.REDIS_IS_DOWN)
