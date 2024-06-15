
import json
from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APIClient, APITestCase

import redis
from authentication.models import Profile, User
from common import variables
from common.utils import BaseTime, authenticate_user, refresh_throttle
from common.variables import *

from .base import BaseUserUnitTestCase


class ProfileViewSetTests(BaseUserUnitTestCase):
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
        self.profile.name = 'Name'
        self.profile.last_name = 'Last name'
        self.profile.save()
        self.url_list = "http://127.0.0.1:8000/user/v1/api/profile/profiles_list/"
        self.url_detail = f"http://127.0.0.1:8000/user/v1/api/profile/{self.profile.pk}/profile_detail/"

    @patch('authentication.v1.apis.profile.ProfileViewSet.permission_classes', return_value=[AllowAny])
    def test_profiles_list_success(self, mock_permission):
        """
        Test retrieving all profiles successfully.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Send a GET request to retrieve all profiles.
        3. Ensure the response status code is 200 OK.
        4. Check that the response contains 'data'.
        5. Ensure the number of profiles in the response matches the number of profiles in the database.
        """
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertEqual(len(response.data['data']), Profile.objects.count())

    @patch('authentication.v1.apis.profile.ProfileViewSet.permission_classes', return_value=[AllowAny])
    def test_profiles_list_empty(self, mock_permission):
        """
        Test retrieving profiles when no profiles exist.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Delete all existing profiles.
        3. Send a GET request to retrieve all profiles.
        4. Ensure the response status code is 200 OK.
        5. Ensure the response contains an empty list of profiles.
        """
        Profile.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)

    @patch('authentication.v1.apis.profile.ProfileViewSet.permission_classes', return_value=[AllowAny])
    def test_profile_detail_success(self, mock_permission):
        """
        Test retrieving a specific profile successfully.

        Procedure:
        1. Mock the permission classes to allow any user.
        2. Send a GET request to retrieve a specific profile.
        3. Ensure the response status code is 200 OK.
        4. Check that the returned profile matches the expected user.
        """
        response = self.client.get(self.url_detail, headers={
                                   'Accept-Language': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['User'], self.user.pk)

