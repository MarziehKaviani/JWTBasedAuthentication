from django.contrib.auth.models import BaseUserManager

from common import variables
from common.variables import PHONE_NUMBER_REQUIRED


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, state=variables.PENDING, **extra_fields):
        if not phone_number:
            raise ValueError(PHONE_NUMBER_REQUIRED)
        user = self.model(phone_number=phone_number,
                          state=state, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, state=variables.PENDING, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, state=state, **extra_fields)
