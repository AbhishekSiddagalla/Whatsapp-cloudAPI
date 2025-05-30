import pytest
import json
from unittest.mock import patch
from send_message_template.whatsapp_cloudapi import WhatsAppMessageSender

@pytest.fixture
def text_media_button_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello from media and button!"}],
        "header_type": "image",
        "media_id": "1234567890",
        "buttons": {
            "type": "url",
            "text": "Click here",
            "url": "https://google.com"
        }
    }

@patch("send_message_template.whatsapp_cloudapi.header_payload", {"image": "/fake/path/to/image.jpg"})
@patch("send_message_template.whatsapp_cloudapi.buttons_payload", {"url": [{"type": "text", "text": "https://google.com"}]})
@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_media_and_button(
    mock_post, mock_template_fetcher, mock_uploader, text_media_button_params
):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    mock_uploader.return_value.upload_media_to_server.return_value = "1234567890"

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "test_template",
            "components": [
                {"type": "HEADER", "format": "IMAGE"},
                {"type": "BODY"},
                {"type": "BUTTONS", "buttons": [{"type": "URL"}]}
            ]
        }
    ]

    sender = WhatsAppMessageSender(**text_media_button_params)

    response = sender.send_message_to_user()

    args, kwargs = mock_post.call_args
    payload = json.loads(kwargs['data'])
    print(payload)

    assert payload["messaging_product"] == "whatsapp"
    assert payload["template"]["name"] == "test_template"

    header_component = next(c for c in payload["template"]["components"] if c["type"] == "header")
    assert header_component["parameters"][0]["type"] == "image"
    assert header_component["parameters"][0]["image"]["id"] == "1234567890"

    body_component = next(c for c in payload["template"]["components"] if c["type"] == "body")
    assert body_component["parameters"][0]["type"] == "text"
    assert body_component["parameters"][0]["text"] == "Hello from media and button!"

    button_component = next(c for c in payload["template"]["components"] if c["type"] == "buttons")
    assert button_component is not None
    assert button_component["parameters"][0]["type"] == "text"
    assert button_component["parameters"][0]["text"] == "https://google.com"

    assert response.status_code == 200
    assert response.json() == {"success": True}
