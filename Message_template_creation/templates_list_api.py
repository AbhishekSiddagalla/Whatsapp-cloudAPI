# fetching all message template names
import requests

from settings import api_version, whatsapp_business_account_id, token

def message_templates_list():
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/message_templates?fields=name,status"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    all_templates = response.json()["data"]

    templates = []
    for template_list in all_templates:
        template_names = template_list["name"]
        templates.append(template_names)

    return templates
