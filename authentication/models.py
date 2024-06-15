from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, Group, Permission,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from redis_service.utils import RedisStore

from .choices import *
from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        # one for +, 7 for maximum len of country code and 10 for maximum national phone number len.
        max_length=18,
        unique=True,
        verbose_name=_(variables.PHONE_NUMBER_VERBOSE_NAME),
    )
    state = models.CharField(
        max_length=32, verbose_name=_("State"), choices=USER_STATE, null=True
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Created at")
    )

    is_bocked = models.BooleanField(
        default=False, verbose_name=_("Is blocked"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group, verbose_name=_("Groups"), blank=True, related_name="user_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("User Permissions"),
        blank=True,
        related_name="user_permissions",
    )

    def __str__(self) -> str:
        return self.phone_number

    # def save(self, *args, **kwargs):
    #     is_new_user = not self.pk
    #     super().save(*args, **kwargs)
    #     if is_new_user:
    #         Profile.objects.create(user=self)

    def block(self):
        """
        Block the user account.
        """
        access_token_lifetime = int(
            str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']).split(' ')[0].strip())
        RedisStore().set(f"blocked:{self.pk}", {
            "phone_number": self.phone_number}, access_token_lifetime * 24 * 60 * 60)
        self.is_bocked = True
        self.save()

    # def unblock(self):
    #     """
    #     Unblock the user account.
    #     """

    #     self.save()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, verbose_name=_('User'))

    name = models.CharField(
        max_length=32, null=True, blank=True, verbose_name=_("Name")
    )
    last_name = models.CharField(
        max_length=32, null=True, blank=True, verbose_name=_("Last name")
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Created at"))

    identity_number = models.CharField(max_length=11, verbose_name=_(
        "Identity Number"), null=True, blank=True)

    birth_date = models.DateField(verbose_name=_(
        "Birth date"), null=True, blank=True)  # TODO Set this too

    father_name = models.CharField(max_length=255, verbose_name=_(
        "Father name"), null=True, blank=True)

    def __str__(self) -> str:
        return self.user.phone_number
