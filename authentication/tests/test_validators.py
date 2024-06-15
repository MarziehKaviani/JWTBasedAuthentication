import pandas as pd
from django.test import TestCase

from authentication.validators import PhoneNumberValidator


class TestIranPhoneNumberValidator(TestCase):
    def setUp(self):
        num_file_path = "numbers_file.txt"
        self.df = self.read_test_numbers(num_file_path)

    def read_test_numbers(self, file_path):
        with open(file_path, "r") as file:
            nums = file.read().split("+")[1:]
        df = pd.DataFrame(
            {"phone_number": nums},
        )
        df.loc[:199, "phone_number"] = df.loc[:199, "phone_number"].str.replace(
            "98-", "00"
        )
        df.loc[200:399, "phone_number"] = df.loc[200:399, "phone_number"].str.replace(
            "98-", "0"
        )
        df.loc[400:599, "phone_number"] = df.loc[400:599, "phone_number"].str.replace(
            "98-", ""
        )
        df.loc[600:799, "phone_number"] = df.loc[600:799, "phone_number"].str.replace(
            "98-", "980"
        )
        df["phone_number"] = df["phone_number"].str.replace("-", "")
        return df

    def validate_phone_number(self, phone_number):
        try:
            PhoneNumberValidator(phone_number)
        except Exception as e:
            return f"Validation failed for phone number {phone_number}: {str(e)}"
        return None

    def test_phone_number_validator(self):
        result_series = self.df["phone_number"].apply(
            lambda x: self.validate_phone_number(x)
        )
        failed_validations = result_series[result_series.notnull()]

        if not failed_validations.empty:
            self.fail(
                f"Validation failed for the following phone numbers: \n{
                    failed_validations.to_string(index=False)}"
            )
