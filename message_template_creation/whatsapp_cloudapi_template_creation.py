# main api for message template creation
import json
import requests

#importing token from settings file
from settings import api_version, whatsapp_business_account_id, api_access_token

def create_message_template(payload):
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/message_templates"
    access_token = api_access_token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = payload

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response