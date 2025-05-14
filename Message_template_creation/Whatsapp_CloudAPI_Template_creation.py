# main api for message template creation
import json
import requests

#importing token from settings file
from settings import api_version, token

whatsapp_business_account_id = "1740776970130492"
def create_message_template(payload):
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/message_templates"
    access_token = token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = payload

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response


