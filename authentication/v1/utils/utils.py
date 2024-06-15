

flags = None


def add_to_permissions(self, permission_list):

    default_permissions = [
        permission() for permission in getattr(self, "permission_classes", [])
    ]
    return default_permissions + permission_list


def normilize_phone_number(validated_phone_number: str, country_code: str):
    return f"00{country_code.strip()}{validated_phone_number.strip()}"
