import random

from decouple import config
from django.shortcuts import get_object_or_404
from django.utils import timezone

from authentication.models import User
from common.utils import BaseTime, SendEmail
from redis_service.utils import RedisStore
from third_party_repository.kavenegar import KavenegarSMSService

otp_adapter = None


def create_verification_code(user):
    """
    Create a verification code for the provided user.

    Parameters:
    ----------
    * `user`: `User`
        The user for whom the verification code needs to be created.

    Returns:
    ----------
    `str`
        The generated verification code.

    Notes:
    ----------
    - A random 6-digit verification code is generated using the characters "0123456789".
    - The code is associated with the provided user, and its expiration time is set to 5 minutes from the current time.
    - The user's `otp_code` and `otp_code_expires` fields are updated, and the code is returned.
    """
    verification_code = "".join(random.choices("0123456789", k=6))
    expiration_timestamp = BaseTime().timedelta(minutes=5)
    return verification_code, expiration_timestamp


class OTPAdapter:
    def __init__(self, ) -> None:
        self.email_service = SendEmail(sender='', source_api='sign_up')
        KAVENEGAR_API_KEY = config("KAVENEGAR_API_KEY", cast=str)
        self.sms_service = KavenegarSMSService(api_key=KAVENEGAR_API_KEY)

    def send_otp(self, otp, phone_number=None, email=None):
        if email:
            self.email_service.send_email(email, otp)
        else:
            self.sms_service.send_sms(receptor=phone_number, otp=otp)


def load_otp_adapter_lazy():
    global otp_adapter
    if otp_adapter is None:
        otp_adapter = OTPAdapter()
    return otp_adapter
