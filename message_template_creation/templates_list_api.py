# fetching all message template names
import requests

from settings import api_version, whatsapp_business_account_id, token


class MessageTemplateFetcher:
    def __init__(self):
        self.api_version = api_version
        self.business_account_id = whatsapp_business_account_id
        self.token = token
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.business_account_id}/message_templates"

    @staticmethod
    def _get_headers(self):
        return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }

    def get_templates_list(self):
        params = {
            "fields": "name,category,parameter_format,language,components,status"
        }

        response = requests.get(self.base_url, headers=self._get_headers(self), params=params).json()
        all_templates = response["data"]
        # print(all_templates)

        return all_templates