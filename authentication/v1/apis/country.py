from rest_framework import status
from rest_framework.views import APIView

from common import variables
from common.utils import BaseResponse
from common.utils import load_countries_lazy


class PhoneNumberCountryViewSet(APIView):
    def get(self, request):
        country_df = load_countries_lazy()[
            [
                variables.NAME,  # TODO there is duplicated name var in variables
                variables.OFFICIAL_NAME,
                variables.ISO_ALPHA_2,
                variables.ISO_ALPHA_3,
                variables.CALLING_CODE,
                variables.NATIONAL_NUMBER_LENGTH,
                variables.FLAG_LINK
            ]
        ]
        return BaseResponse(
            message=None,
            data=country_df.to_dict(orient=variables.RECORDS),
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            business_status_code=variables.BUSINESS_STATUS.SUCCESS,
        )
