from settings import sender_phone_number, to_phone_number
from whatsapp_cloudapi import WhatsAppMessageSender

class WhatsAppMessageService:
    def __init__(self):
        self.sender_phone_number = sender_phone_number
        self.to_phone_number = to_phone_number

    def service_to_user(self):
        # fetching all approved templates from the fetch_templates method
        all_templates = WhatsAppMessageSender(self).fetch_templates()

        print("Available Templates:")

        for template in all_templates:
            if template["status"] == "APPROVED":
                print(template["name"], "---", template["parameter_format"], "---", template["category"], "---",
                      template["status"])

        # creating a list of template names
        template_list = [template["name"] for template in all_templates]

        # getting user input for the template name
        template_name = input("\nEnter template name from the above list: ").strip()
        if template_name not in template_list:
            return print(f"{template_name} is invalid. Please try again.")

        # fetching template name from the template list
        selected_template = next(template for template in all_templates if template["name"] == template_name)
        print(selected_template)
        # getting the body component from the selected template
        body_component = next((component for component in selected_template["components"] if component["type"] == "BODY"), None)

        print("Message preview:\n", body_component["text"])

        placeholder_count = body_component["text"].count("{{")

        placeholders = []
        if placeholder_count > 0:
            print("\nEnter values for the following placeholders:")
            for i in range(1,placeholder_count + 1):
                user_input = input("Enter placeholder {%d} :" %i).strip()
                placeholders.append(user_input)

        print("\nSender phone number:", self.sender_phone_number)
        print("Recipient phone number:", self.to_phone_number)

        header_part = next((c for c in selected_template["components"]if c["type"] == "HEADER"),None)

        # print(header_part["text"])

        sender = WhatsAppMessageSender(
                        template_name=template_name,
                        template_params= [{"type": "text", "text": value} for value in placeholders]
                                       )

        response = sender.send_message_to_user().json()
        return print(response)

    def template_selection(self):
        print("Welcome to WhatsApp Cloud API")
        print("=" * 50)
        print("Choose one of the following options:")
        print("1. Create a new template")
        print("2. Select from the approved template list")

        try:
            user_choice = int(input("Enter your choice: "))
        except ValueError:
            return print("Invalid input. Please enter a number.")

        if user_choice == 1:
            return "In progress..."
        elif user_choice == 2:
            return self.service_to_user()
        else:
            return print("Invalid choice. Please try again.")

send_message = WhatsAppMessageService().template_selection()