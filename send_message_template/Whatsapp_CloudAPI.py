#sending message template to User using Cloud API
import requests
import json

#importing token from settings file
from settings import api_version, token, to_phone_number
from sender_phone_number.sender_phone_numbers_list import WhatsAppPhoneNumberFetcher

phone_number_id = WhatsAppPhoneNumberFetcher().get_phone_number_id()


class WhatsAppMessageSender:
    def __init__(self,template_name,template_params=None):
        self.api_version = api_version
        self.phone_number_id = phone_number_id
        self.token = token
        self.to_phone_number = to_phone_number
        self.template_name = template_name
        self.template_params = template_params or []
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get_payload(self):
        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_phone_number,
            "type": "template",
            "template": {
                "name": self.template_name,
                "language": {"code": "en_US"}
            }
        }

        # Only add components if there are parameters
        if self.template_params:
            payload["template"]["components"] = [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": param} for param in self.template_params]
                }
            ]

        return payload

    def send_message_to_user(self):
        headers = self._get_headers()
        payload = self._get_payload()

        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
        return response