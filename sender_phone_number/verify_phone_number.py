# verifying a phone number whether it is a valid number or not
import requests

from settings import api_version, phone_number_id, whatsapp_business_account_id, token


def get_phone_numbers_list():
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/phone_numbers?access_token={token}"
    response = requests.get(url)
    phone_numbers = response.json()
    return phone_numbers

print(get_phone_numbers_list())


def requesting_code():
    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/request_code"