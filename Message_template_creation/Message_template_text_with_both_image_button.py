from Whatsapp_CloudAPI_Template_creation import create_message_template

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
                    "header_handle": [
                        "https://bgcchecktest.s3.us-east-1.amazonaws.com/1/SampleJPGImage_200kbmb.jpg"
                    ]
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