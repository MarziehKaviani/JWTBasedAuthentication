from django.utils.translation import gettext_lazy as _

MUST_BE_ANON = _('User must be anonymous')

INVALID_OTP = _("Invalid verification code provided")

USER_DONT_HAVE_OTP = _(
    "There is no created otp for the user with provided phone number, request one first or check the phone number.")

PHONE_NUMBER_REQUIRED = _("The Phone number field must be set")

USER_DONT_HAVE_ACCESS = _("User dont have access to perform this action")

INVALID_LOGIN_CRED = _("Invalid Phone_number or verification code")

EXPIRED_VERIFICATION_CODE = _('Verification code has expired')

USER_ALREADY_EXISTS = _("User with this phone number already exists")

USER_DOSE_NOT_EXISTS = _(
    "User with this phone number dose not exists. Please register first.")

USER_REGISTERD = _(
    "User registered successfully. Check your phone for the verification code")

ALREADY_LOGGED_OUT = _("The user is already logged out")

VERIFICATION_CODE_SENDED = _(
    "Verification code sended successfilly. Check your phone for the Code")

BLOCKED_USER = _(
    "User with this phone number is blocked and cant perform this action anymore.")

INVALID_INPUT_DATA = _("Invalid input data")

USER_LOGGED_IN = _("User verified and logged in successfully")

USER_LOGGED_OUT = _("User logged out successfully")

INVALID_COUNTRY_CODE = _("Invalid country code")

INVALID_PHONE_NUMBER = _("Invalid phone number")

ANON_TOKEN_CREATED = _("Anonymous token created successfully.")

USER_IS_NOT_VERIFIED = _("User didn't complete identity verification")

USER_INFO_NOT_MATCHED = _("The given data not matches for this user")

INVALID_USER_INFO = _("The given data is not valid")

USER_VERIFIED_SUCCESSFULLY = _("User verified successfully")

USER_TO_MANY_TRY = _("You've reached your usage limit")

TRY_AGAIN_LATER = _("Something went wrong. Please try again later")


class BusinessStatusCodes:
    """
    1000-1999 for user-related errors
    2000-2999 for payment-related errors
    3000-3999 for validation errors
    4000-4999 for system errors
    5000-5100 for zibal
    """
    USER_IS_BLOCKED = 1001
    USER_NOT_FOUND = 1001
    USER_DONT_HAVE_ACCESS = 1003
    USER_IS_NOT_VERIFIED = 1004
    USER_INFO_NOT_MATCHED = 1005
    INVALID_USER_DATA = 1006
    SUCCESS = 200
    INVALID_INPUT_DATA = 3001
    INVALID_LOGIN_CREDENTIONAL = 3002
    ZIBAL_HAS_EXCEPTION = 5000
    ZIBAL_TOO_MANY_REQUEST = 5001
    REDIS_IS_DOWN = 4001


BUSINESS_STATUS = BusinessStatusCodes()

# Static Key
ZIBAL_TOKEN = "ZIBAL_TOKEN"
CONTENT_TYPE = "Content-Type"
AUTHORIZATION = "Authorization"
MOBILE = "mobile"
ZIBAL_NATIONAL_CODE = "nationalCode"
ZIBAL_BIRTH_DATE = "birthDate"
BIRTH_DATE = "birth_date"
NATIONAL_CODE = 'national_code'
NATIONAL_ID = 'nationalId'
BIRTH_DATE = "birth_date"
POST = "POST"
GET = "GET"
IDENTITY_CODE = "identity_code"
APPLICATION_JSON = "application/json"
PHONE_NUMBER = 'phone_number'
PHONE_NUMBER_VERBOSE_NAME = 'Phone number'
COUNTRY_CODE = "country_code"
COUNTRY_CODE_VERBOSE_NAME = "Country code"
VERIFICATION_CODE = "verification_code"
VERIFICATION_CODE_VERBOSE_NAME = 'Verification code'
ERROR = "error"
DETAILS = "details"
SUCCESS = 'success'
REFRESH = 'refresh'
ACCESS = 'access'
REFRESH_TOKEN = 'refresh_token'
ACCESS_TOKEN = 'access_token'
ANON_TOKEN = 'anon_token'
NAME = 'Name'
OFFICIAL_NAME = 'OfficialName'
ISO_ALPHA_2 = 'IsoAlpha2'
ISO_ALPHA_3 = 'IsoAlpha3'
CALLING_CODE = 'CallingCode'
NATIONAL_NUMBER_LENGTH = 'NationalNumberLength'
FLAG_LINK = 'FlagLink'
RECORDS = 'records'
NAME = "name"
SOURCE = "source"
MESSAGE = "message"
LEVEL = "level"
PENDING = "pending"
PHONE_VERIFIED = "phone_verified"
USER_VERIFIED = "user_verified"
DELETED = "deleted"
PERSONAL_INFO = 'personal_info'
COMPANY_INFO = 'COMPANY_INFO'
COUNT = 'count'
EXPIRTION_TIME = 'expirtion_time'
ZIBAL_BASE_URL = "https://api.zibal.ir"
CONFIRMATION_TOKEN = 'confirmation_token'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
FATHER_NAME = 'father_name'
ALIVE = 'alive'
IDENTITY_NUMBER = 'identity_number'
IS_REDIRECT = "IS_REDIRECT"
FATAL_EXCEPTION = "Fatal exception"
