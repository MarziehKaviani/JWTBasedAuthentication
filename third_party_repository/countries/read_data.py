import subprocess

import pandas as pd
from decouple import config
from django.conf import settings

from common.owncloud import owncloud_handler

base_dir = settings.BASE_DIR

BASE_LINK = None


def add_flag_link(x):
    x['FlagLink'] = f'{BASE_LINK}/download?path=&files={x["IsoAlpha2"]}.svg'
    return x


def get_countries_df(columns=['Name', 'OfficialName', 'Capital', 'Language', 'CallingCode', 'NationalNumberLength', 'Currency', 'Flag', 'IsoAlpha2', 'IsoAlpha3']):
    OWNCLOUD_ADMIN_PASSWORD = config("OWNCLOUD_ADMIN_PASSWORD", cast=str)
    OWNCLOUD_ADMIN_USERNAME = config("OWNCLOUD_ADMIN_USERNAME", cast=str)
    OWNCLOUD_FLAGS_DIRECTORY_PATH = config(
        "OWNCLOUD_FLAGS_DIRECTORY_PATH", cast=str)
    global BASE_LINK
    if not BASE_LINK:
        BASE_LINK = owncloud_handler.generate_upload_link_with_token(
            OWNCLOUD_ADMIN_USERNAME, OWNCLOUD_ADMIN_PASSWORD, OWNCLOUD_FLAGS_DIRECTORY_PATH, 120)
    df = pd.read_csv(
        f'{base_dir}/third_party_repository/countries/country_data.csv')
    df = df[df['isIndependent'] == 'Yes'][columns]
    df.loc[df['Name'] == 'Namibia', 'IsoAlpha2'] = 'NA'
    df_with_flags = df.apply(add_flag_link, axis=1)
    return df_with_flags
