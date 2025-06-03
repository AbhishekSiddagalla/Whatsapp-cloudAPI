from whatsapp_cloudapi_template_creation import create_message_template

def msg_template_with_text_and_button():

    payload = {
        "name": "track_order",
        "category": "UTILITY",
        "language": "en_US",
        "components": [
            {
                "type": "HEADER",
                "format": "text",
                "text": "Here is Order Details"
            },
            {
                "type": "BODY",
                "text": "Your Order is on its way. To track order status, click on the button below."
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
                        "url": "https://www.facebook.com"
                    }
                ]
            }
        ]
    }
    result = create_message_template(payload)
    print(result.json())

msg_template_with_text_and_button()