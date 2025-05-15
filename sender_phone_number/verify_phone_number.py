# verifying a phone number whether it is a valid number or not
import requests

from settings import api_version, whatsapp_business_account_id, token
from sender_phone_number.sender_phone_numbers_list import phone_number_id


def requesting_code():
    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/request_code"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "code_method": "sms",
        "language": "en"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.json()

# print(requesting_code())

# verifying a phone number whether it is a valid number or not
def verify_phone_number():
    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/verify_code"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "code": ""
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.json()

# print(verify_phone_number())