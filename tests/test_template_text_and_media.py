# message template with text and media
import pytest
import json
from unittest.mock import patch
from send_message_template import whatsapp_cloudapi
from send_message_template.whatsapp_cloudapi import WhatsAppMessageSender


@pytest.fixture
def text_and_media_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello with media!"}],
        "header_type": "image",
    }


@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_and_media(mock_post, mock_template_fetcher, mock_uploader, text_and_media_params):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    mock_uploader.return_value.upload_media_to_server.return_value = "1234567890"

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "test_template",
            "components": [
                {"type": "HEADER", "format": "IMAGE"},
                {"type": "BODY"}
            ]
        }
    ]


    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/fake/path/to/image.jpg"}):
        sender = WhatsAppMessageSender(**text_and_media_params)
        response = sender.send_message_to_user()

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs["data"])

        assert payload["messaging_product"] == "whatsapp"
        assert payload["template"]["name"] == "test_template"

        components = payload["template"]["components"]
        header_component = next(c for c in components if c["type"] == "header")
        body_component = next(c for c in components if c["type"] == "body")

        assert header_component["parameters"][0]["type"] == "image"
        assert header_component["parameters"][0]["image"]["id"] == "1234567890"
        assert body_component["parameters"][0]["type"] == "text"
        assert body_component["parameters"][0]["text"] == "Hello with media!"

@pytest.fixture
def invalid_media_id_payload():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello"}],
        "header_type": "image",
        "media_id": "INVALID_ID"
    }

@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_template_with_invalid_media_id_format(mock_post, mock_template_fetcher, mock_uploader,invalid_media_id_payload):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Invalid media ID"}

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "test_template",
            "components": [{"type": "HEADER", "format": "IMAGE"}]
        }
    ]

    mock_uploader.return_value.upload_media_to_server.return_value = "INVALID_ID"

    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/image/path.jpg"}):
        sender = WhatsAppMessageSender(**invalid_media_id_payload)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()
