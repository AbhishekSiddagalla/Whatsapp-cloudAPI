import requests

from settings import api_version, whatsapp_business_account_id, token, sender_phone_number

# fetching all sender's phone numbers

class WhatsAppPhoneNumberFetcher:
    def __init__(self):
        self.api_version = api_version
        self.whatsapp_business_account_id = whatsapp_business_account_id
        self.token = token
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.whatsapp_business_account_id}/phone_numbers"
        self.sender_phone_number = sender_phone_number

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }
    def get_phone_number_id(self):
        params = {"access_token": self.token}
        response = requests.get(self.base_url,params=params)

        if response.status_code == 200:
            data = response.json()
            for item in data.get("data", []):
                if item.get("display_phone_number") == self.sender_phone_number:
                    return item.get("id")

            raise Exception(f"Phone number {self.sender_phone_number} not found.")

        else:
            raise Exception(f"Failed to fetch phone numbers. Status Code: {response.status_code}, Response: {response.text}")
