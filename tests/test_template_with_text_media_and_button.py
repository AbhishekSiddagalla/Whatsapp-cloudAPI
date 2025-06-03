import pytest
import json

from unittest.mock import patch

from send_message_template import whatsapp_cloudapi
from send_message_template.whatsapp_cloudapi import WhatsAppMessageSender

@pytest.fixture
def text_media_button_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello from media and button!"}],
        "header_type": "image",
        "media_id": "1234567890",
    }

#Test: template with valid data
@patch("send_message_template.whatsapp_cloudapi.header_payload", {"image": "/fake/path/to/image.jpg"})
@patch("send_message_template.whatsapp_cloudapi.buttons_payload", {"url": [{"type": "url", "text": "Visit", "url": "https://example.com"}]})
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
    assert body_component["parameters"][0]["text"] == "{'type': 'text', 'text': 'Hello from media and button!'}"

    button_component = next(c for c in payload["template"]["components"] if c["type"].lower() == "button")
    assert button_component["sub_type"] == "URL"
    assert "parameters" in button_component

    assert response.status_code == 200
    assert response.json() == {"success": True}

@pytest.fixture
def nonexistent_template_payload():
    return {
        "template_name": "nonexistent_template",
        "template_params": [{"type": "text", "text": "Test"}],
        "header_type": "image"
    }

# Test: template with no template name
@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_template_not_found(mock_post, mock_template_fetcher, mock_uploader, nonexistent_template_payload):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Template not found"}

    mock_template_fetcher.return_value.get_templates_list.return_value = []

    with patch.dict(whatsapp_cloudapi.header_payload, {"image": "/some/image.jpg"}):
        sender = WhatsAppMessageSender(**nonexistent_template_payload)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()


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
def test_template_with_invalid_media_id_format(mock_post, mock_template_fetcher, mock_uploader, invalid_media_id_payload):
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

@pytest.fixture
def template_payload_with_invalid_button_data():
    return {
        "template_name": "invalid_template",
        "template_params": [{"type": "text", "text": "test"}],
        "header_type": "image"
    }

@patch("send_message_template.whatsapp_cloudapi.WhatsAppMediaUploader")
@patch("send_message_template.whatsapp_cloudapi.MessageTemplateFetcher")
@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_invalid_button_parameter(mock_post, mock_template_fetcher, mock_uploader, template_payload_with_invalid_button_data):
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
        sender = WhatsAppMessageSender(**template_payload_with_invalid_button_data)
        response = sender.send_message_to_user()

        assert response.status_code == 400
        assert "error" in response.json()
