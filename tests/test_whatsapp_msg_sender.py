# Scenario : testing whatsappmessagesender api without params

import pytest
import json
from unittest.mock import patch
from send_message_template.whatsapp_cloudapi import WhatsAppMessageSender  # Update path as needed

# message template with only text
@pytest.fixture
def text_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello, user!"}],
    }

@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_only(mock_post, text_params):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    sender = WhatsAppMessageSender(**text_params)
    response = sender.send_message_to_user()

    # Extract payload sent to requests.post
    args, kwargs = mock_post.call_args
    payload = json.loads(kwargs['data'])

    assert payload["messaging_product"] == "whatsapp"
    assert payload["template"]["name"] == "test_template"
    assert payload["template"]["components"][0]["type"] == "body"
    assert payload["template"]["components"][0]["parameters"][0]["text"] == "Hello, user!"

    # Validate mock response
    assert response.status_code == 200
    assert response.json() == {"success": True}

# message template with text and media

@pytest.fixture
def text_and_media_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello with media!"}],
        "header_type": "image",
        "header_text": None,
        "media_id": "1234567890"
    }

@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_and_media(mock_post, text_and_media_params):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    sender = WhatsAppMessageSender(**text_and_media_params)
    response = sender.send_message_to_user()

    #Extract payload sent to requests.post
    args, kwargs = mock_post.call_args
    payload = json.loads(kwargs['data'])

    assert payload["messaging_product"] == "whatsapp"
    assert payload["template"]["name"] == "test_template"
    header_component = payload["template"]["components"][0]

    assert header_component["type"] == "header"
    assert header_component["parameters"][0]["type"] == "image"
    assert header_component["parameters"][0]["image"]["id"] == "1234567890"

    assert response.status_code == 200
    assert response.json() == {"success": True}