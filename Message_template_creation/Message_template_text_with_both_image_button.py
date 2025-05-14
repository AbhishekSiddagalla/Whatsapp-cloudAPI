from Whatsapp_CloudAPI_Template_creation import create_message_template
from media_upload_api.image_upload_api import upload_image_to_server

image_handle = upload_image_to_server()

def msg_template_text_with_both_image_and_button():

    payload = {
        "name": "tracking_order",
        "category": "UTILITY",
        "language": "en_US",
        "components": [
            {
                "type": "HEADER",
                "format": "IMAGE",
                "example": {
                    "header_handle": [image_handle]
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
    result = create_message_template(payload)
    print(result.json())

msg_template_text_with_both_image_and_button()