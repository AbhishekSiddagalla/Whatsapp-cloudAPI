# main api for message template creation
import json
import requests

#importing token from settings file
from settings import api_version, whatsapp_business_account_id, api_access_token
from media_upload_api.media_uploader import HeaderHandle

handle_value = HeaderHandle()


class MessageTemplateCreator:
    def __init__(self):
        self.url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/message_templates"
        self.headers = {
            "Authorization": f"Bearer {api_access_token}",
            "Content-Type": "application/json"
        }
        self.header_handle = handle_value.get_header_handle()


    def get_header_component(self, header_format, header_text):
        if header_format.upper() == "TEXT":
            return {
                "type": "HEADER",
                "format": "TEXT",
                "text": header_text
            }
        elif header_format.upper() in ["IMAGE", "VIDEO", "DOCUMENT"]:
            return {
                "type": "HEADER",
                "format": header_format,
                "example": {
                    "header_handle": [self.header_handle]
                }
            }
        return None
    @staticmethod
    def get_buttons_component(buttons):
        button_list = []
        for button in buttons:
            if button["type"].upper() == "URL":
                button_list.append({
                    "type": "URL",
                    "text": button["text"],
                    "url": button["url"]
                })
            elif button["type"].upper() == "PHONE_NUMBER":
                button_list.append({
                    "type": "PHONE_NUMBER",
                    "text": button["text"],
                    "phone_number": button["phone_number"]
                })
        return {
            "type": "BUTTONS",
            "buttons": button_list
        }
    def create_template_with_payload(self, name, header_format, header_text, body_text, footer_text, buttons, body_example_params):
        components = []

        #add a header component
        if header_format:
            components.append(
                self.get_header_component(header_format, header_text)
            )
        #add body
        body_component = {
            "type": "BODY",
            "text": body_text
        }
        # if there are placeholders in the message template
        if body_example_params:
            body_component["example"] = {
                "body_text" : body_example_params
            }
        components.append(body_component)
        #add footer
        if footer_text:
            components.append({
                "type": "FOOTER",
                "text": footer_text
            })
        #add buttons
        if buttons:
            components.append(self.get_buttons_component(buttons))

        payload = {
            "name": name,
            "category": "UTILITY",
            "language": "en_US",
            "components": components
        }

        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return response.json()