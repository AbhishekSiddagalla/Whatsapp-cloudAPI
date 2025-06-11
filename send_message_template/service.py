import re

from settings import sender_phone_number, to_phone_number
from whatsapp_cloudapi import WhatsAppMessageSender
from message_template_creation.whatsapp_cloudapi_template_creation import MessageTemplateCreator

template_creator = MessageTemplateCreator()


class WhatsAppMessageService:
    def __init__(self):
        self.sender_phone_number = sender_phone_number
        self.to_phone_number = to_phone_number

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
            return self.create_new_template()
        elif user_choice == 2:
            return self.service_to_user()
        else:
            return print("Invalid choice. Please try again.")

    #extracting placeholder values
    @staticmethod
    def extract_placeholders(text):
        return re.findall(r"{{\d+}}",text)

    def create_new_template(self):
        template_name = input("Enter template name:").strip()
        #if a user passes an empty field
        if template_name is None:
            return f"{template_name} is invalid"

        #header part
        header_format = input("Enter Header format (TEXT/IMAGE/VIDEO/DOCUMENT):").strip().upper()
        header_text = None
        if header_format == "TEXT":
            header_text = str(input("Enter header text:"))

        #body part
        body_text = str(input("Enter body text (use placeholders {{1}}, {{2}},...):"))
        body_placeholders = self.extract_placeholders(body_text)
        body_example_params = []        #creating an empty list to store placeholder values
        if body_placeholders:
            for placeholder in body_placeholders:
                place_holder_value = str(input(f"Enter placeholder {placeholder}:"))
                body_example_params.append(place_holder_value)  #adding all placeholders

        #footer part
        add_footer = input("Do you want to add footer(YES/NO)? :").strip().lower()
        footer_text = None
        if add_footer == "yes":
            footer_text = str(input("Enter footer text(Optional):"))

        # add buttons
        buttons = []
        add_button = input("Do you want to add button(YES/NO)? :").strip().lower()
        if add_button == "yes":
            button_type = input("Enter button type(URL/PHONE_NUMBER):").strip().upper()
            button_text = str(input("Enter button text:").strip())

            if button_type == "URL":
                url = input("Enter URL:").strip()
                buttons.append({
                    "type": "URL",
                    "text": button_text,
                    "url": url
                })
            elif button_type == "PHONE_NUMBER":
                phone_number = str(input("Enter phone number with country code (+91):")).strip()
                buttons.append({
                    "type": "PHONE_NUMBER",
                    "text": button_text,
                    "phone_number": str(phone_number)
                })

        #previewing the message template before creating
        print("\n TEMPLATE PREVIEW")
        print(f"Template Name:{template_name}\n")
        if header_format == "TEXT":
            print(header_text)
        print(body_text)
        if body_placeholders:
            print(f"placeholders={body_example_params}")
        if footer_text:
            print(footer_text)
        if buttons:
            print(buttons)

        preview_confirmation = input("Do you want to proceed with this template? (YES/NO):").strip().lower()
        if preview_confirmation == "yes":
            create_template = template_creator.create_template_with_payload(
                template_name,
                header_format,
                header_text,
                body_text,
                footer_text,
                buttons,
                body_example_params
            )
            return print(create_template)
        return None
    def get_approved_templates(self):
        all_templates = WhatsAppMessageSender(self).fetch_templates()
        approved_templates = [template for template in all_templates if template["status"] == "APPROVED"]
        return approved_templates

    @staticmethod
    def user_template_selection(templates):
        print("Available Templates:\n")
        for template in templates:
            print(
                f"{template['name']} --- {template['parameter_format']} --- "
                f"{template['category']} --- {template['status']}"
            )

        template_names = [template["name"] for template in templates]
        template_name = input("\nEnter template name from the above list: ").strip()

        if template_name not in template_names:
            print(f"{template_name} is invalid. Please try again.")
            return None

        return next(template for template in templates if template["name"] == template_name)

    @staticmethod
    def get_template_placeholders(text):
        placeholder_count = text.count("{{")
        placeholders = []

        if placeholder_count > 0:
            print("\nEnter values for the following placeholders:")
            for i in range(1, placeholder_count + 1):
                user_input = input("Enter placeholder {{%d}}: "%i).strip()
                placeholders.append(user_input)

        return placeholders

    @staticmethod
    def preview_message(header, body, placeholders):
        print("\nMessage preview:\n")

        if header and header.get("format") == "TEXT":
            print(header["text"])
        elif header:
            print(f"Header format: {header['format']} (media link required)")

        filled_message = body["text"]
        for i, value in enumerate(placeholders, start=1):
            filled_message = filled_message.replace("{{%d}}" % i, value)

        print(filled_message)
        return filled_message

    def send_confirmed_message(self, template_name, placeholders):
        print("\nSending message...")
        print("Sender phone number:", self.sender_phone_number)
        print("Recipient phone number:", self.to_phone_number)

        sender = WhatsAppMessageSender(
            template_name=template_name,
            template_params=placeholders
        )

        response = sender.send_message_to_user().json()
        print("Response from WhatsApp API:")
        print(response)

    def service_to_user(self):
        approved_templates = self.get_approved_templates()

        selected_template = self.user_template_selection(approved_templates)
        if not selected_template:
            return "Invalid template."

        header = next((c for c in selected_template["components"] if c["type"] == "HEADER"), None)
        body = next((c for c in selected_template["components"] if c["type"] == "BODY"), None)

        if not body:
            return print("Invalid template format: BODY not found.")

        print("\nMessage preview with placeholders:\n")
        if header and header.get("format") == "TEXT":
            print(header["text"])
        elif header:
            print(f"Header format: {header['format']} (media link required)")

        print(body["text"])

        placeholders = self.get_template_placeholders(body["text"])

        print("\nMessage preview with filled values:")
        self.preview_message(header, body, placeholders)

        confirmation = input("\nEnter 'YES' to send the message or 'NO' to cancel: ").strip().lower()
        if confirmation == "no":
            return print("Restart the process.")
        elif confirmation == "yes":
            return self.send_confirmed_message(selected_template["name"], placeholders)
        else:
            return print("Invalid input. Process stopped.")


# Run the service
send_message = WhatsAppMessageService().template_selection()
