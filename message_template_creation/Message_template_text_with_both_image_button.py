from Whatsapp_CloudAPI_Template_creation import create_message_template
from media_upload_api.document_upload_api import HeaderHandle

handle_value = HeaderHandle()
header_handle = handle_value.get_header_handle()

def msg_template_text_with_both_image_and_button():

    payload = {
        "name": "test_image_and_button",
        "category": "UTILITY",
        "language": "en_US",
        "components": [
            {
                "type": "HEADER",
                "format": "IMAGE",
                "example": {
                    "header_handle": [header_handle]
                }
            },
            {
                "type": "BODY",
                "text": "Good News, You order is on its way. To track order status, click on the button below."
            },
            {
                "type": "FOOTER",
                "text": "Contact support if this wasn't you."
            },
            {
                "type": "BUTTONS",
                "buttons":[
                    {
                        "type": "URL",
                        "text": "Track Order",
                        "url": "https://www.google.com"
                    }
                ]
            }
        ]
    }
    result = create_message_template(payload).json()
    print(result)

msg_template_text_with_both_image_and_button()