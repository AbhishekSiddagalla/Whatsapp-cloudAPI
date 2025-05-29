import requests
import json

from message_template_creation.templates_list_api import MessageTemplateFetcher
from settings import api_version, token, to_phone_number
from sender_phone_number.sender_phone_numbers_list import WhatsAppPhoneNumberFetcher
from media_upload_api.media_uploader import WhatsAppMediaUploader
from message_template_payload import header_payload

phone_number_id = WhatsAppPhoneNumberFetcher().get_phone_number_id()


class WhatsAppMessageSender:
    def __init__(self, template_name, template_params=None, header_text=None):
        self.template_list = []
        self.header_text = header_text
        self.api_version = api_version
        self.phone_number_id = phone_number_id
        self.token = token
        self.to_phone_number = to_phone_number
        self.template_name = template_name
        self.template_params = template_params or []
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    # fetching all message templates list
    def fetch_templates(self):
        self.template_list = MessageTemplateFetcher().get_templates_list()

        return self.template_list

    # headers to be passed in the url
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    #data or body to be passed in the url
    def _get_payload(self):
        body_params = self.template_params

        template_list = self.fetch_templates()
        selected_template = next((template for template in template_list if template["name"] == self.template_name),None)

        header_type = None
        if selected_template:
            header_component = next((c for c in selected_template.get("components", []) if c["type"].upper() == "HEADER"), None)
            if header_component:
                header_format = header_component.get("format").lower()
                header_type = header_format

        # Build header parameters based on the detected header type
        header_params = []
        if header_type in ["image", "video", "document"]:
            # Get the file path from header_payload
            media_file = header_payload.get(header_type)
            if media_file:
                media_id = WhatsAppMediaUploader().upload_media_to_server(
                    media_file_path=media_file,
                    header_type=header_type
                )
                if media_id:
                    header_params.append({
                        "type": header_type,
                        header_type: {
                            "id": media_id
                        }
                    })

            # Handle text headers separately
        elif header_type == "text":
            text_value = header_payload.get("text")
            if text_value:
                header_params.append({
                    "type": "text",
                    "text": text_value
                })

        button_params = []

        components = []
        #message template Header Part
        if header_params:
            components.append({
                "type": "header",
                "parameters": header_params
            })
        #message template Body part
        if body_params:
            components.append({
                "type": "body",
                "parameters": body_params
            })

        if button_params:
            components.extend({
                "type": "button",
                "sub_type": "PHONE_NUMBER",
                "parameters": button_params
            })

        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_phone_number,
            "type": "template",
            "template": {
                "name": self.template_name,
                "language": {"code": "en_US"},
                "components": components
            }
        }

        return payload

    def send_message_to_user(self):
        headers = self._get_headers()
        payload = self._get_payload()
        res = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
        return res

