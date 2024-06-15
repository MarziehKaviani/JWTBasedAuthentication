import json

import urllib3
from decouple import config
from rest_framework import status

from common.variables import *
from third_party_repository.models.ZibalModels import CompanyInfo

ZIBAL_BASE_URL = "https://api.zibal.ir"


class VerificationPhoneNumberWithIdentityCodeResponse:
    def __init__(self, message, matched, result):
        self.message = message
        self.matched = matched
        self.result = result

    def __getitem__(self):
        return {
            "message": self.message,
            "matched": self.matched,
            "result": self.result,
        }

    def __str__(self):
        return str({
            "message": self.message,
            "matched": self.matched,
            "result": self.result,
        }
        )


class GetPrivacyInfosResponse:
    def __init__(self, first_name, last_name, father_name, alive):
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name
        self.alive = alive

    def __getitem__(self):
        alive_status = "زنده" if self.alive else "فوت شده"
        return {NAME: self.first_name,
                        LAST_NAME: self.last_name,
                        FATHER_NAME: self.father_name,
                        ALIVE: alive_status}

    def __str__(self):
        alive_status = "زنده" if self.alive else "فوت شده"
        return (f"{NAME}: {self.first_name}\n"
                f"{LAST_NAME} {self.last_name}\n"
                f"{FATHER_NAME} {self.father_name}\n"
                f"{ALIVE}: {alive_status}")


def parse_response(response):
    if response["result"] == 1 and response["data"]["nationalCode"]:
        data = response["data"]
        person = GetPrivacyInfosResponse(
            first_name=data["firstName"],
            last_name=data["lastName"],
            father_name=data["fatherName"],
            alive=data["alive"]
        )
        return person
    else:
        return None


class ZibalService:

    def __init__(self, token) -> None:
        self.token = token
        self.http = urllib3.PoolManager()

    def verify_phone_number_with_identity_code(self, phone_number, identity_code):
        url = f"{ZIBAL_BASE_URL}/v1/facility/shahkarInquiry/"
        payload = json.dumps({
            MOBILE: f"0{phone_number[4:]}",
            ZIBAL_NATIONAL_CODE: identity_code
        }).encode('utf-8')
        headers = {
            AUTHORIZATION: self.token,
            CONTENT_TYPE: APPLICATION_JSON
        }

        response = self.http.request(POST, url, headers=headers, body=payload)

        if response.status == status.HTTP_200_OK:
            data = json.loads(response.data.decode('utf-8'))
            verification_res = VerificationPhoneNumberWithIdentityCodeResponse(
                message=data['message'],
                matched=data['data']['matched'],
                result=data['result']
            )
            return verification_res
        else:
            # print(
            #     f"Error: HTTP {response.status} - {response.data.decode('utf-8')}")
            return None

    def get_personal_infos(self, identity_code, birth_date):
        url = f"{ZIBAL_BASE_URL}/v1/facility/nationalIdentityInquiry"
        payload = json.dumps({
            ZIBAL_NATIONAL_CODE: identity_code,
            ZIBAL_BIRTH_DATE: birth_date
        }).encode('utf-8')
        headers = {
            AUTHORIZATION: self.token,
            CONTENT_TYPE: APPLICATION_JSON
        }

        response = self.http.request(POST, url, headers=headers, body=payload)
        if response.status == status.HTTP_200_OK:
            data = json.loads(response.data.decode('utf-8'))
            personal_info = parse_response(data)
            return personal_info
        else:
            # print(
            #     f"Error: HTTP {response.status} - {response.data.decode('utf-8')}")
            return None

    def get_company_infos(self, national_id: str):
        url = f"{ZIBAL_BASE_URL}/v1/facility/companyInquiry"
        payload = json.dumps({
            NATIONAL_ID: national_id
        }).encode('utf-8')
        headers = {
            AUTHORIZATION: self.token,
            CONTENT_TYPE: APPLICATION_JSON
        }
        response = self.http.request(POST, url, headers=headers, body=payload)

        if response.status == status.HTTP_200_OK:
            res = json.loads(response.data.decode('utf-8'))
            return res
        else:
            # print(
            #     f"Error: HTTP {response.status} - {response.data.decode('utf-8')}")
            return None
