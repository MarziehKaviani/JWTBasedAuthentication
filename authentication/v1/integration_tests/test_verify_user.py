import redis
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework.permissions import AllowAny

from authentication.models import Profile
from common.utils import BaseResponse
from common.validators import check_api_input_data
from common.variables import *
from common.variables import BUSINESS_STATUS
from common import variables
from common.utils import BaseTime
from third_party_repository.ZibalApi import ZibalService
from authentication.models import Profile
from third_party_repository.ZibalApi import \
    VerificationPhoneNumberWithIdentityCodeResponse
from redis_service.utils import RedisStore


class VerifyUserIntegrationTest(APITestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = get_user_model().objects.create(phone_number='00989131234567')
        self.profile = Profile.objects.create(user=self.user)

        # Set up the client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Define URLs
        self.verify_user_url = "http://127.0.0.1:8000/user/v1/api/verify_user/"
        self.show_preview_url = "http://127.0.0.1:8000/user/v1/api/verify_user/show_preview/"
        self.confirm_informations_url = 'http://127.0.0.1:8000/user/v1/api/verify_user/confirm_informations/'

    def tearDown(self):
        # Flush the Redis database to clean up after tests
        RedisStore().flush()

    @patch("third_party_repository.ZibalApi.ZibalService.get_personal_infos")
    @patch("third_party_repository.ZibalApi.ZibalService.verify_phone_number_with_identity_code")
    @patch('authentication.v1.apis.verify_user.VerifyUserViewSet.permission_classes', return_value=[AllowAny])
    def test_verify_user_flow(self, mock_permission, mock_zibal_verification_phone, mock_get_personal_info):
        # Step 1: Verify user information
        verify_data = {
            NATIONAL_CODE: '1234567894',
            BIRTH_DATE: '1381-07-26',
            PHONE_NUMBER: '9131234567',
            COUNTRY_CODE: '98',
        }
        mock_zibal_verification_phone.return_value = VerificationPhoneNumberWithIdentityCodeResponse(
        message='موفق', matched=True, result=1)
        mock_get_personal_info.return_value = {
            variables.PHONE_NUMBER: "9131234567",
            variables.PERSONAL_INFO: {
                "first_name": "Name",
                "last_name": "Last name"
            },
            variables.COUNT: 1,
            variables.IDENTITY_NUMBER: '1234567894'
        }
        response = self.client.post(self.verify_user_url, data=verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(PERSONAL_INFO, response.data['data'])
        
        # Step 2: Show preview data
        response = self.client.get(self.show_preview_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(PERSONAL_INFO, response.data['data'])

        # Step 3: Confirm information and update profile
        confirm_data = {CONFIRMATION_TOKEN: self.user.pk}
        response = self.client.post(self.confirm_informations_url, data=confirm_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[MESSAGE], USER_VERIFIED_SUCCESSFULLY)

        # Check if the profile is updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.identity_number, '9131234567')
        self.assertEqual(str(self.profile.birth_date), '1381-07-26')

if __name__ == "__main__":
    import unittest
    unittest.main()