import requests
import json

from message_template_creation.templates_list_api import MessageTemplateFetcher
from settings import api_version, api_access_token, to_phone_number
from sender_phone_number.sender_phone_numbers_list import WhatsAppPhoneNumberFetcher
from media_upload_api.media_uploader import WhatsAppMediaUploader
from send_message_template.message_template_payload import header_payload

phone_number_id = WhatsAppPhoneNumberFetcher().get_phone_number_id()


class WhatsAppMessageSender:
    def __init__(self, template_name, template_params=None, header_text=None, header_type=None, media_id=None):
        self.template_name = template_name
        self.template_params = template_params or []
        self.header_text = header_text
        self.header_type = header_type
        self.media_id = media_id

        self.api_version = api_version
        self.token = api_access_token
        self.to_phone_number = to_phone_number
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    def fetch_templates(self):
        """Fetch all templates using the external fetcher class."""
        return MessageTemplateFetcher().get_templates_list()

    def _get_headers(self):
        """Return request headers."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get_selected_template(self):
        """Return the selected template object by name."""
        templates = self.fetch_templates()
        return next((t for t in templates if t["name"] == self.template_name), None)

    def _prepare_body_params(self):
        """Convert each body placeholder into the required format."""
        return [{"type": "text", "text": str(param)} for param in self.template_params]

    def _prepare_header_params(self, header_component):
        """create header parameters depending on the format."""
        header_format = header_component.get("format", "").lower()
        header_params = []

        if header_format in ["image", "video", "document"]:
            media_file = header_payload.get(header_format)
            if media_file:
                media_id = WhatsAppMediaUploader().upload_media_to_server(
                    media_file_path=media_file,
                    header_type=header_format
                )
                if media_id:
                    header_params.append({
                        "type": header_format,
                        header_format: {"id": media_id}
                    })

        elif header_format == "text":
            if "{{" in header_component.get("text", ""):
                text_value = header_payload.get("text")
                if text_value:
                    header_params.append({
                        "type": "text",
                        "text": text_value["text"]
                    })

        return header_format, header_params

    def _prepare_components(self, selected_template):
        """Assemble the complete list of components for the payload."""
        components = []

        # HEADER
        header_component = next((c for c in selected_template.get("components", []) if c["type"].upper() == "HEADER"), None)
        if header_component:
            _, header_params = self._prepare_header_params(header_component)
            if header_params:
                components.append({
                    "type": "header",
                    "parameters": header_params
                })

        # BODY
        body_params = self._prepare_body_params()
        if body_params:
            components.append({
                "type": "body",
                "parameters": body_params
            })

        return components

    def _get_payload(self):
        """Create the payload JSON structure for sending a message."""
        selected_template = self._get_selected_template()
        if not selected_template:
            raise ValueError(f"Template '{self.template_name}' not found.")

        components = self._prepare_components(selected_template)

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
        """Send the composed template message to the user."""
        headers = self._get_headers()
        payload = self._get_payload()

        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
        return response
