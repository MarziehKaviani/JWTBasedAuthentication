import inspect
import os
import subprocess
import textwrap
from datetime import datetime, timedelta
from subprocess import call

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd
from django.conf import settings

from third_party_repository.countries.read_data import get_countries_df
from authentication.models import User
from common.variables import INVALID_INPUT_DATA

root_dir_path = settings.BASE_DIR

BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def authenticate_user(user='009121234567'):
    user = User.objects.create(phone_number=user, otp_code="123456")
    access = str(RefreshToken.for_user(user).access_token)
    return {"Authorization": f"Bearer {access}"}


def refresh_throttle():
    setattr(AnonRateThrottle, "THROTTLE_RATES", {"anon": "100/sec"})
    setattr(UserRateThrottle, "THROTTLE_RATES", {"user": "100/sec"})


def get_caller_name():
    stack = inspect.stack()
    calling_frame = stack[2]
    calling_function_name = calling_frame[3]
    return calling_function_name


def _print(text, color_code):
    print(f"{color_code}{text}{RESET}")


class ExecuteTerminalCommand:
    def __init__(self, command, path=os.getcwd()) -> None:
        self.execute_command(command, path)

    def add_tab_in_lines(self, output):
        wrapped_output = textwrap.indent(
            textwrap.fill(output, width=80), "   ")
        return f"{wrapped_output}"

    def execute_command(self, command, path):
        os.chdir(path)
        try:

            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=path
            )
            _print(self.add_tab_in_lines(result.stdout), GREEN)
        except subprocess.CalledProcessError as e:
            _print(self.add_tab_in_lines(e.stderr), RED)


class SendEmail:
    def __init__(self, sender, source_api) -> None:
        self.sender = sender
        self.source_api = source_api

    def send_email(receptor, message):
        pass


def list_to_choices(arr):
    return tuple([(i[1], _(i[1])) for i in arr])


def test_headers(user='09121234567'):
    headers = authenticate_user(user)
    headers['Accept-Language'] = 'en'
    return headers


def get_validated_data_from_serializer(serializer: serializers.Serializer, data: dict):
    serializer = serializer(data=data)
    if serializer.is_valid():
        return serializer.validated_data
    else:
        raise {"error": INVALID_INPUT_DATA, "details": serializer.errors,
               "status": 400, }


class BaseResponse(Response):
    def __init__(self,  http_status_code, is_exception, message='Unknown', business_status_code=-1, data=None) -> None:
        super().__init__(
            data={
                "data": data,
                "message": message,
                'business_status_code': business_status_code
            },
            status=http_status_code,
            exception=is_exception
        )


class BaseTime:
    @staticmethod
    def now() -> float:
        """
        Get the current time as a Unix timestamp.
        """
        return datetime.now().timestamp()

    @staticmethod
    def timedelta(days=0, seconds=0, microseconds=0,
                  milliseconds=0, minutes=0, hours=0, weeks=0) -> float:
        """
        Calculate a future time as a Unix timestamp given a timedelta.
        """
        current_time = datetime.now()
        future_time = current_time + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                               milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
        return future_time.timestamp()


cities_df = None
countries_df = None

countries_hints_dict = {
    "1": "",  # TODO complete these 5 one
    "1809": '',
    "39": '',
    "76": '',
    "7": '',
    "3906698": '',
    '93': '+..-..-...-....',
    '355': '+...(...)...-...',
    '213': '+...-..-...-....',
    '1684': '+.(...)...-....',
    '376': '+...-...-...',
    '244': '+...(...)...-...',
    '1264': '+.(...)...-....',
    '1268': '+.(...)...-....',
    '54': '+..(...)...-....',
    '374': '+...-..-...-...',
    '297': '+...-...-....',
    '61': '+.. ... ... ...',
    '43': '+..(...)...-....',
    '994': '+...-..-...-..-..',
    '1242': '+.(...)...-....',
    '973': '+...-....-....',
    '880': '+...-..-...-...',
    '1246': '+.(...)...-....',
    '375': '+...(..)...-..-..',
    '32': '+.. ... .. .. ..',
    '501': '+...-...-....',
    '229': '+...-..-..-....',
    '1441': '+.(...)...-....',
    '975': '+...-.-...-...',
    '591': '+...-.-...-....',
    '387': '+...-..-....',
    '267': '+...-..-...-...',
    '55': '+..-..-....-....',
    '246': '+...-...-....',
    '1284': '+.(...)...-....',
    '673': '+...-...-....',
    '359': '+...(...)...-...',
    '226': '+...-..-..-....',
    '257': '+...-..-..-....',
    '855': '+...-..-...-...',
    '237': '+...-....-....',
    '238': '+...(...)..-..',
    '1345': '+.(...)...-....',
    '236': '+...-..-..-....',
    '235': '+...-..-..-..-..',
    '56': '+..-.-....-....',
    '86': '+.. ..-........',
    '57': '+..(...)...-....',
    '269': '+...-..-.....',
    '243': '+...(...)...-...',
    '242': '+...-..-...-....',
    '682': '+...-..-...',
    '506': '+... ....-....',
    '225': '+...-..-...-...',
    '385': '+...-..-...-...',
    '53': '+..-.-...-....',
    '357': '+...-..-...-...',
    '420': '+...(...)...-...',
    '45': '+.. .. .. .. ..',
    '253': '+...-..-..-..-..',
    '1767': '+.(...)...-....',
    '593': '+...-.-...-....',
    '20': '+..(...)...-....',
    '503': '+... ....-....',
    '240': '+...-..-...-....',
    '291': '+...-.-...-...',
    '372': '+...-...-....',
    '251': '+...-..-...-....',
    '500': '+...-.....',
    '298': '+...-...-...',
    '679': '+...-..-.....',
    '358': '+... .. .... ....',
    '33': '+.. . .. .. .. ..',
    '594': '+...-.....-....',
    '689': '+...-..-..-..',
    '241': '+...-.-..-..-..',
    '220': '+...(...)..-..',
    '995': '+...(...)...-...',
    '49': '+.. ... .......',
    '233': '+...(...)...-...',
    '350': '+...-...-.....',
    '30': '+..(...)...-....',
    '299': '+...-..-..-..',
    '1473': '+.(...)...-....',
    '1671': '+.(...)...-....',
    '502': '+... ....-....',
    '224': '+...-..-...-...',
    '245': '+...-.-......',
    '592': '+...-...-....',
    '509': '+... ....-....',
    '504': '+...-....-....',
    '852': '+... .... ....',
    '36': '+..(...)...-...',
    '354': '+... ... ....',
    '91': '+.. .....-.....',
    '62': '+..-..-...-..',
    '98': '+..(...)...-....',
    '964': '+...(...)...-....',
    '353': '+... .. .......',
    '972': '+...-.-...-....',
    '1876': '+.(...)...-....',
    '81': '+.. ... .. ....',
    '962': '+...-.-....-....',
    '254': '+...-...-......',
    '686': '+...-..-...',
    '965': '+...-....-....',
    '996': '+...(...)...-...',
    '856': '+...-..-...-...',
    '371': '+...-..-...-...',
    '961': '+...-.-...-...',
    '266': '+...-.-...-....',
    '231': '+...-..-...-...',
    '218': '+...-..-...-...',
    '423': '+...(...)...-....',
    '370': '+...(...)..-...',
    '352': '+...(...)...-...',
    '853': '+...-....-....',
    '389': '+...-..-...-...',
    '261': '+...-..-..-.....',
    '265': '+...-.-....-....',
    '60': '+.. ..-....-....',
    '960': '+...-...-....',
    '223': '+...-..-..-....',
    '356': '+...-....-....',
    '692': '+...-...-....',
    '596': '+...(...)..-..-..',
    '222': '+...-..-..-....',
    '230': '+...-...-....',
    '52': '+..-..-..-....',
    '691': '+...-...-....',
    '373': '+...-....-....',
    '377': '+...-..-...-...',
    '976': '+...-..-..-....',
    '382': '+...-..-...-...',
    '1664': '+.(...)...-....',
    '212': '+...-..-....-...',
    '258': '+...-..-...-...',
    '95': '+..-...-...',
    '264': '+...-..-...-....',
    '674': '+...-...-....',
    '977': '+...-..-...-...',
    '31': '+.. .. ........',
    '687': '+...-..-....',
    '64': '+.. ...-...-....',
    '505': '+...-....-....',
    '227': '+...-..-..-....',
    '234': '+...-..-...-..',
    '683': '+...-....',
    '672': '+...-...-...',
    '850': '+...-...-...',
    '1670': '+.(...)...-....',
    '47': '+.. ... .. ...',
    '968': '+...-..-...-...',
    '92': '+.. ...-.......',
    '680': '+...-...-....',
    '970': '+...-..-...-....',
    '507': '+...-...-....',
    '675': '+...(...)..-...',
    '595': '+...(...)...-...',
    '51': '+..(...)...-...',
    '63': '+.. ... ....',
    '48': '+.. ...-...-...',
    '351': '+...-..-...-....',
    '974': '+...-....-....',
    '262': '+...-.....-....',
    '40': '+..-..-...-....',
    '250': '+...(...)...-...',
    '1869': '+.(...)...-....',
    '1758': '+.(...)...-....',
    '1784': '+.(...)...-....',
    '685': '+...-..-....',
    '378': '+...-....-......',
    '239': '+...-..-.....',
    '966': '+...-..-...-....',
    '221': '+...-..-...-....',
    '381': '+...-..-...-....',
    '248': '+...-.-...-...',
    '232': '+...-..-......',
    '65': '+.. ....-....',
    '1721': '+.(...)...-....',
    '421': '+...(...)...-...',
    '386': '+...-..-...-...',
    '677': '+...-.....',
    '252': '+...-.-...-...',
    '27': '+..-..-...-....',
    '82': '+..-..-...-....',
    '211': '+...-..-...-....',
    '34': '+.. ... ... ...',
    '94': '+..-..-...-....',
    '249': '+...-..-...-....',
    '597': '+...-...-...',
    '268': '+...-..-..-....',
    '46': '+.. .. ... .. ..',
    '41': '+.. .. ... .. ..',
    '963': '+...-..-....-...',
    '886': '+...-....-....',
    '992': '+...-..-...-....',
    '255': '+...-..-...-....',
    '66': '+..-..-...-...',
    '670': '+...-...-....',
    '228': '+...-..-...-...',
    '690': '+...-....',
    '676': '+...-.....',
    '1868': '+.(...)...-....',
    '216': '+...-..-...-...',
    '90': '+.. ... ... .. ..',
    '993': '+...-.-...-....',
    '1649': '+.(...)...-....',
    '688': '+...-.....',
    '1340': '+.(...)...-....',
    '256': '+...(...)...-...',
    '380': '+...(..)...-..-..',
    '971': '+...-.-...-....',
    '44': '+.. .... ......',
    '598': '+...-.-...-..-..',
    '998': '+...-..-...-....',
    '678': '+...-.....',
    '58': '+..(...)...-....',
    '84': '+..-..-....-...',
    '681': '+...-..-....',
    '212': '+...-..-....',
    '967': '+...-.-...-...',
    '260': '+...-..-...-....',
    '263': '+...-.-.....'
}


def load_cities_lazy():
    global cities_df
    if cities_df is None:
        cities_df = pd.read_csv(f'{settings.BASE_DIR}/assets/cities.csv')
    return cities_df


def load_countries_lazy():
    global countries_df
    if countries_df is None:
        countries_df = get_countries_df()
    return countries_df


def get_countries_list(columns):
    df: pd.DataFrame = load_countries_lazy()[columns]
    country_list = df.to_dict(orient='records')
    for idx, country in enumerate(country_list):
        country['id'] = idx
    return country_list


def get_flags():
    df = load_countries_lazy()[['Name', 'IsoAlpha2', 'FlagLink']]
    country_list = df.to_dict(orient='records')
    return country_list


def get_cities_list(country_iso2_code=None):
    df: pd.DataFrame = load_cities_lazy()
    if country_iso2_code:
        unique_cities = df[df['country_code'] == str(country_iso2_code).strip()][[
            'id', 'name']].drop_duplicates().dropna()
    else:
        unique_cities = df[['id', 'name']
                           ].drop_duplicates().dropna()  # all cities
    cities_list = [tuple(x) for x in unique_cities.to_numpy()]
    return cities_list
