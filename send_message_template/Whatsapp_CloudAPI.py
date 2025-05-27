#sending message template to User using Cloud API
import requests
import json

from message_template_creation.templates_list_api import MessageTemplateFetcher
from settings import api_version, token, to_phone_number, sender_phone_number
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
        body_params = self.template_params

        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_phone_number,
            "type": "template",
            "template": {
                "name": self.template_name,
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "body",
                        "parameters": body_params
                    },
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
        self.sender_phone_number = sender_phone_number
        self.to_phone_number = to_phone_number

    def fetch_template_names(self):
        self.template_list = MessageTemplateFetcher().get_templates_list()
        print("Available Templates:")

        for template in self.template_list:
            if template["status"] == "APPROVED":
                print("-", template["name"], template["status"], template["category"],
                      template["parameter_format"])

        return self.template_list

    def send_message_to_user(self):

        all_templates = self.fetch_template_names()
        template_list = [template_names["name"] for template_names in all_templates ]

        template_name = str(input("Enter template name from the above list:")).strip()

        if template_name not in template_list:
            return f"{template_name} is invalid. Please try again."

        # Get selected template details
        selected_template = next(template for template in all_templates if template["name"] == template_name)

        # Extract parameter names from the 'body_text_named_params'
        body_component = next((component for component in selected_template["components"] if comp["type"] == "BODY"), None)

        if not body_component or "example" not in body_component or "body_text_named_params" not in body_component[
            "example"]:
            return print("Template doesn't have proper named parameter examples. Please check template configuration.")

        #Fetching Parameter names
        named_params = body_component["example"]["body_text_named_params"]
        print(f"Template '{template_name}' expects the following parameters:")

        template_params = []
        for param in named_params:
            param_name = param["param_name"]
            value = input(f"Enter value for '{param_name}': ").strip()
            template_params.append({"type": "text", "parameter_name": param_name, "text": value})

        print("\nSender phone number:", self.sender_phone_number)
        print("Recipient phone number:", self.to_phone_number)

        sender = WhatsAppMessageSender(template_name, template_params)
        response = sender.send_message_to_user().json()

        return print(response)


    def template_selection(self):
        print("Welcome to WhatsApp Cloud API")
        print("="*50)
        print("Choose one of the following options:")
        print("1. Create a new template")
        print("2. Select from the approved template list")

        user_choice = int(input("enter your choice:"))

        if user_choice == 1:
            pass
        elif user_choice == 2:
            return self.send_message_to_user()

        return print("Invalid choice. Please try again.")


send_message = WhatsAppMessageService().template_selection()




