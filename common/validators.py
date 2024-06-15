from django.http.request import QueryDict


def check_api_input_data(request, required_fields=None, optional_fields=None):
    data = dict()
    request_data = request.data
    if required_fields:
        for field in required_fields:
            if field not in request_data:
                return False
            data[field] = request_data[field]
    if optional_fields:
        for field in optional_fields:
            if field not in request_data:
                return False
        data[field] = request_data[field]
    if type(request_data) == QueryDict:  # Type of data in tests, is querydict
        request_data = request_data.dict()
    return data == request_data
