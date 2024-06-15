import warnings
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework.test import APITestCase

from authentication.choices import *
from authentication.models import Profile, User
from authentication.v1.utils.otp import create_verification_code
from authentication.v1.utils.token import generate_token
from common import variables


class BaseUserUnitTestCase(APITestCase):
    def setUp(self):
        settings.SESSION_ENGINE = "django.contrib.sessions.backends.file"
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning,
        )
        self.factory = RequestFactory()
        self.anon_token = self.get_anon_token()
        self.user = self.create_user()
        self.profile = Profile.objects.create(user=self.user)
        access_token = self.get_access_token()
        self.headers = {"Authorization": f"{access_token}", }

    def get_anon_token(self):
        self.client.user = AnonymousUser()
        anon_token = generate_token(self.client)["anon_token"]
        self.session["anon_token"] = anon_token
        self.session.save()
        return anon_token

    def get_access_token(self):
        self.user.state = variables.PHONE_VERIFIED
        self.user.save()
        return generate_token(self.client, self.user)["access"]

    def create_user(self, phone_number="00989121234567"):
        user = User.objects.create(phone_number=phone_number)
        create_verification_code(user)
        return user
