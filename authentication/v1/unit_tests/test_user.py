from unittest.mock import patch

from rest_framework import status
from rest_framework.permissions import AllowAny

from authentication.v1.apis import *
from authentication.v1.serializers import *
from common.permissions import IsNotBlocked
from common.utils import refresh_throttle
from common.variables import *

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
        self.user = User.objects.create(phone_number='00989131234567')

    def test_blocked_user_access(self):
        sample_api_url = "http://127.0.0.1:8000/user/v1/api/profile/profiles_list/"
        self.client.force_authenticate(user=self.user)
        self.user.block()
        response = self.client.get(sample_api_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            'You do not have permission to perform this action.', response.data['detail'])
