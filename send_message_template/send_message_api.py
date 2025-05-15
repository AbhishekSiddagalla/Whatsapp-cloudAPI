# api to call all the apis to send a message

from Message_template_creation.templates_list_api import message_templates_list
from send_message_template.Whatsapp_CloudAPI import send_whatsapp_message

def send_message_api():
    # to_phone_number = str(input("Enter Receiver's phone number:"))

    template_list = message_templates_list()
    print(template_list)

    template_name = str(input("Enter template name from the above list:"))

    response = send_whatsapp_message()
    if response.status_code == 200:
        print(f"{template_name} Message sent successfully.")

send_message_api()