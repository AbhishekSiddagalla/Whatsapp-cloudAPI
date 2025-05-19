# api to call all the apis to send a message

from message_template_creation.templates_list_api import MessageTemplateFetcher
from send_message_template.Whatsapp_CloudAPI import WhatsAppMessageSender

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

        response = sender.send_message_to_user()
        return response.json()

send_message = WhatsAppMessageService().send_message_to_user()

print("message sent successfully")
print(send_message)