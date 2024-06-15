class CompanyInfo:
    def __init__(self, national_id, company_title, company_registration_id, establishment_date, address, zipcode, status, company_related_people):
        self.national_id = national_id
        self.company_title = company_title
        self.company_registration_id = company_registration_id
        self.establishment_date = establishment_date
        self.address = address
        self.zipcode = zipcode
        self.status = status
        self.company_related_people = company_related_people

    @classmethod
    def from_dict(cls, data):
        # print(f"data : {data}")
        return cls(
            national_id=data['nationalId'],
            company_title=data['companyTitle'],
            company_registration_id=data['companyRegistrationId'],
            establishment_date=data['establishmentDate'],
            address=data['address'],
            zipcode=data['zipcode'],
            status=data['status'],
            company_related_people=[
                PersonalInfo.from_dict(person) for person in data['companyRelatedPeople']
            ]
        )


class PersonalInfo:
    def __init__(self, first_name, last_name, national_code, office_position):
        self.first_name = first_name
        self.last_name = last_name
        self.national_code = national_code
        self.office_position = office_position

    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data['firstName'],
            last_name=data['lastName'],
            national_code=data['nationalCode'],
            office_position=data['officePosition']
        )
