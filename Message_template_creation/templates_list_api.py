# fetching all message template names
import requests

from settings import api_version, whatsapp_business_account_id, token

def message_templates_list():
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/message_templates?fields=name,status"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    templates = response.json()
    return templates

print(message_templates_list())