#creating a message template with text
from whatsapp_cloudapi_template_creation import create_message_template

def msg_template_with_text():

    payload = {
        "name": "order_confirmation",
        "category": "UTILITY",
        "language": "en_US",
        "components": [
            {
                "type": "HEADER",
                "format": "text",
                "text": "Order Confirmed"
            },
            {
                "type": "BODY",
                "text": "Your order has been confirmed. Invoice will be sent soon."
            },
            {
                "type": "FOOTER",
                "text": "contact support if you have any questions."
            }
        ]
    }
    result = create_message_template(payload)
    print(result.json())

msg_template_with_text()