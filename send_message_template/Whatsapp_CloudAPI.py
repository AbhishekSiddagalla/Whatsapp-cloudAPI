#sending message template to User using Cloud API
import requests
import json

from message_template_creation.templates_list_api import MessageTemplateFetcher
from settings import api_version, token, to_phone_number
from sender_phone_number.sender_phone_numbers_list import WhatsAppPhoneNumberFetcher
from media_upload_api.document_upload_api import WhatsAppMediaUploader

phone_number_id = WhatsAppPhoneNumberFetcher().get_phone_number_id()

media_id = WhatsAppMediaUploader().upload_document_to_server()

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
                "name": "test_image_and_button",
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "id": media_id
                                }
                            }
                        ]
                    }
                ]
            }
        }

        return payload

    def send_message_to_user(self):
        headers = self._get_headers()
        payload = self._get_payload()

        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
        return response

class WhatsAppMessageService:
    def __init__(self):
        self.template_list = []

    def fetch_template_names(self):
        self.template_list = MessageTemplateFetcher().get_templates_list()
        print("Available Templates:")

        for template in self.template_list:
            print("-", template)

    def send_message_to_user(self):
        self.fetch_template_names()

        template_name = str(input("Enter template name from the above list:")).strip()
        sender = WhatsAppMessageSender(template_name)

        response = sender.send_message_to_user().json()
        return response

send_message = WhatsAppMessageService().send_message_to_user()
print(send_message)
