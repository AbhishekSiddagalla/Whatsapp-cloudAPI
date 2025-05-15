#sending message template to User using Cloud API
import requests
import json

#importing token from settings file
from settings import api_version, token, to_phone_number
from sender_phone_number.sender_phone_numbers_list import phone_number_id

def send_whatsapp_message():
    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone_number,
        "type": "template",
        "template": {
            "name": "track_order",
            "language": {
                "code": "en_US"
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return response


