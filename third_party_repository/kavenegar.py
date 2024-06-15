import urllib3


class KavenegarSMSService:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.http = urllib3.PoolManager()

    def send_sms(self, otp, receptor):
        url = f"https://api.kavenegar.com/v1/{self.api_key}/verify/lookup.json?receptor={receptor}&token={otp}&template=verify"
        try:
            response = self.http.request(
                "GET",
                url,
                headers={
                    "Cookie": "cookiesession1=678A8C3102ACFHJKLMNOPQRSTUVW853C"},
            )
        except Exception as e:
            print(f"Error: {e}")


# if __name__ == "__main__":
#     from decouple import config

#     KAVENEGAR_API_KEY = config("KAVENEGAR_API_KEY", cast=str)
#     KavenegarSMSService(KAVENEGAR_API_KEY).send_otp_sms("123456", "09139145398")
