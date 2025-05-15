# Registering a phone number to WhatsApp business account
import requests

from settings import api_version, whatsapp_business_account_id, token


def phone_number_registration():
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/register"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "messaging_product": "whatsapp",
        "pin": "123456",
        "data_localization_region": "IN"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

print(phone_number_registration())