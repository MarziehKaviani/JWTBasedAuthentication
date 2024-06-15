from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from common import variables
from common.utils import BaseTime


class IntegrationLoginTestCase(APITestCase):

    def setUp(self):
        """
        Prepare the environment for each test case in the integration login flow.

        This method is executed before each individual test method and is used to
        set up initial conditions such as defining the URLs for API endpoints and
        initializing the APIClient instance.

        Setup Steps:
        1. Initialize the APIClient instance.
        2. Define the URLs for the anonymous token, verification code, and login endpoints.
        """
        self.client = APIClient()
        self.anonymous_token_url = "http://127.0.0.1:8000/user/v1/api/anonymous_user/generate_token/"
        self.verification_code_url = "http://127.0.0.1:8000/user/v1/api/verification_code/get/"
        self.login_url = "http://127.0.0.1:8000/user/v1/api/login/"

    def test_end_to_end_login_flow_new_user(self):
        """
        Test the end-to-end login flow for a new user.

        This test verifies the complete login process for a new user, including
        generating an anonymous token, requesting a verification code, and logging
        in with the verification code.

        Procedure:
        1. Generate an anonymous token by sending a GET request to the anonymous token API endpoint.
           - Verify that the response status code is 200 OK.
           - Confirm that the response message indicates the anonymous token was created successfully.
        2. Request a verification code by sending a POST request to the verification code API endpoint with the user's phone number and country code.
           - Mock the `create_verification_code` function to return a valid verification code and expiration time.
           - Mock the `send_otp` function to simulate sending the OTP without actual sending.
           - Verify that the response status code is 201 Created.
           - Confirm that the response message indicates the user is registered and OTP is sent.
        3. Mock the Redis `get` method to return the correct OTP and expiration time for the user.
        4. Log in with the OTP by sending a POST request to the login API endpoint with the user's phone number, country code, and verification code.
           - Verify that the response status code is 200 OK.
           - Confirm that the response message indicates the user has logged in successfully.
           - Ensure the response contains the access and refresh tokens.
        """
        # 1. Generate an Anonymous Token
        response = self.client.get(self.anonymous_token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(variables.ANON_TOKEN_CREATED, response.data['message'])

        # # Set the anonymous token in the client session for further requests
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['data'])

        # 2. Request Verification Code
        phone_number = "9123456789"
        country_code = "98"
        data = {
            variables.PHONE_NUMBER: phone_number,
            variables.COUNTRY_CODE: country_code
        }

        with patch("authentication.v1.utils.otp.create_verification_code", return_value=("123456", 300)):
            with patch("authentication.v1.apis.login.send_otp") as mock_send_otp:
                mock_send_otp.return_value = None
                response = self.client.post(self.verification_code_url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(variables.USER_REGISTERD, response.data['message'])

        # Mock the Redis get call to return the correct OTP and expiration time
    
        with patch("redis_service.utils.RedisStore.get", return_value={
            variables.VERIFICATION_CODE: "123456",
            variables.EXPIRTION_TIME: BaseTime().now() + 300
        }) as mock_redis_get:

            # 3. Login with OTP
            login_data = {
                variables.PHONE_NUMBER: phone_number,
                variables.COUNTRY_CODE: country_code,
                variables.VERIFICATION_CODE: "123456"
            }

            response = self.client.post(self.login_url, login_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(variables.USER_LOGGED_IN, response.data['message'])
            self.assertIn(variables.REFRESH_TOKEN, response.data['data'].keys())
            self.assertIn(variables.ACCESS_TOKEN, response.data['data'].keys())

    def test_end_to_end_login_flow_existing_user(self):
        """
        Test the end-to-end login flow for an existing user.

        This test verifies the complete login process for an existing user, including
        generating an anonymous token, requesting a verification code, and logging
        in with the verification code.

        Procedure:
        1. Create a user with a known phone number in the system.
        2. Generate an anonymous token by sending a GET request to the anonymous token API endpoint.
           - Verify that the response status code is 200 OK.
           - Confirm that the response message indicates the anonymous token was created successfully.
        3. Request a verification code by sending a POST request to the verification code API endpoint with the user's phone number and country code.
           - Mock the `create_verification_code` function to return a valid verification code and expiration time.
           - Mock the `send_otp` function to simulate sending the OTP without actual sending.
           - Verify that the response status code is 200 OK.
           - Confirm that the response message indicates the verification code was sent successfully.
        4. Mock the Redis `get` method to return the correct OTP and expiration time for the user.
        5. Log in with the OTP by sending a POST request to the login API endpoint with the user's phone number, country code, and verification code.
           - Verify that the response status code is 200 OK.
           - Confirm that the response message indicates the user has logged in successfully.
           - Ensure the response contains the access and refresh tokens.
        """
        # Step 1: Create an existing user
        get_user_model().objects.create(phone_number="00989123456789")

        # Step 2: Generate an Anonymous Token
        response = self.client.get(self.anonymous_token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(variables.ANON_TOKEN_CREATED, response.data['message'])

        # Step 3: Request Verification Code
        phone_number = "9123456789"
        country_code = "98"
        data = {
            variables.PHONE_NUMBER: phone_number,
            variables.COUNTRY_CODE: country_code
        }

        with patch("authentication.v1.utils.otp.create_verification_code", return_value=("123456", 300)):
            with patch("authentication.v1.apis.login.send_otp") as mock_send_otp:
                mock_send_otp.return_value = None
                response = self.client.post(self.verification_code_url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(variables.VERIFICATION_CODE_SENDED, response.data['message'])

        # Step 4: Mock the Redis get call to return the correct OTP and expiration time
        with patch("redis_service.utils.RedisStore.get", return_value={
            variables.VERIFICATION_CODE: "123456",
            variables.EXPIRTION_TIME: BaseTime().now() + 300
        }) as mock_redis_get:

            # Step 5: Login with OTP
            login_data = {
                variables.PHONE_NUMBER: phone_number,
                variables.COUNTRY_CODE: country_code,
                variables.VERIFICATION_CODE: "123456"
            }

            response = self.client.post(self.login_url, login_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(variables.USER_LOGGED_IN, response.data['message'])
            self.assertIn(variables.REFRESH_TOKEN, response.data['data'].keys())
            self.assertIn(variables.ACCESS_TOKEN, response.data['data'].keys())