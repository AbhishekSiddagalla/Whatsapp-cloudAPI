import pytest
import json

from unittest.mock import patch

from send_message_template import whatsapp_cloudapi
from send_message_template.whatsapp_cloudapi import WhatsAppMessageSender

@pytest.fixture
def text_with_placeholders():
    return {
        "template_name": "template_with_placeholders",
        "template_params": [{"type": "text", "text": "body placeholders"}],
        "header_type": "image"
    }

@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_media_and_static_button(mock_post, mock_template_fetcher, mock_uploader, text_with_placeholders):
    # Mock POST response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    # Mock media upload
    mock_uploader.return_value.upload_media_to_server.return_value = "media_id_67890"

    # Mock template definition with header, body with placeholder, and a URL button
    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "combo_template_static_button",
            "components": [
                {"type": "HEADER", "format": "IMAGE"},
                {"type": "BODY"},
                {"type": "BUTTONS", "buttons": [{"type": "URL", "url": "https://example.com"}]}
            ]
        }
    ]

    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/fake/path/image.jpg"}):
        sender = WhatsAppMessageSender(**text_with_placeholders)
        response = sender.send_message_to_user()

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs["data"])

        assert payload["messaging_product"] == "whatsapp"
        assert payload["template"]["name"] == "template_with_placeholders"

        components = payload["template"]["components"]

        header_component = next(c for c in components if c["type"].lower() == "header")
        body_component = next(c for c in components if c["type"].lower() == "body")
        button_component = next(c for c in components if c["type"].lower() == "button")

        assert header_component["parameters"][0]["type"] == "image"
        assert header_component["parameters"][0]["image"]["id"] == "media_id_67890"

        assert body_component["parameters"][0]["type"] == "text"
        assert body_component["parameters"][0]["text"] == "body placeholders"

        assert button_component["sub_type"] == "URL"
        assert "parameters" in button_component

        assert response.status_code == 200
        assert response.json() == {"success": True}

@pytest.fixture
def template_payload_with_invalid_data():
    return {
        "template_name": "invalid_template",
        "template_params": [{"type": "text", "text": "test"}],
        "header_type": "image"
    }

# Test: Header type is invalid or unsupported
@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_invalid_header_type(mock_post, mock_template_fetcher, mock_uploader, template_payload_with_invalid_data):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Invalid header type"}

    mock_uploader.return_value.upload_media_to_server.return_value = None

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "invalid_template",
            "components": [{"type": "HEADER", "format": "UNSUPPORTED_FORMAT"}]
        }
    ]

    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/fake/path.jpg"}):
        sender = WhatsAppMessageSender(**template_payload_with_invalid_data)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()

# Test: Media upload fails
@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_media_upload_fails(mock_post, mock_template_fetcher, mock_uploader, template_payload_with_invalid_data):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Bad Request"}

    # Media upload returns None
    mock_uploader.return_value.upload_media_to_server.return_value = None

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "invalid_template",
            "components": [{"type": "HEADER", "format": "IMAGE"}]
        }
    ]

    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/invalid/path.jpg"}):
        sender = WhatsAppMessageSender(**template_payload_with_invalid_data)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()


# Test: Invalid button parameter
@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_invalid_button_parameter(mock_post, mock_template_fetcher, mock_uploader, template_payload_with_invalid_data):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {
        "error": {
            "message": "template['components'][2]['parameters'][0] must be a JSON object.",
            "code": 100
        }
    }

    mock_uploader.return_value.upload_media_to_server.return_value = "media_id_123"

    mock_template_fetcher.return_value.get_templates_list.return_value = [
        {
            "name": "invalid_template",
            "components": [
                {"type": "HEADER", "format": "IMAGE"},
                {"type": "BODY"},
                {"type": "BUTTONS", "buttons": [{"type": "URL"}]}
            ]
        }
    ]

    # Provide invalid buttons payload
    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/some/path/image.jpg"}), \
            patch.dict(whatsapp_cloudapi.buttons_payload, {"url": "invalid_button_string"}):
        sender = WhatsAppMessageSender(**template_payload_with_invalid_data)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()
