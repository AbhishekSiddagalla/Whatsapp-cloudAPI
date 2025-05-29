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


# test_send_message_with_text_media_button.py

@pytest.fixture
def text_media_button_params():
    return {
        "template_name": "test_template",
        "template_params": [{"type": "text", "text": "Hello from media and button!"}],
        "header_type": "image",
        "header_text": None,
        "media_id": "1234567890",
        "button": {
            "type": "url",
            "text": "Click here",
            "url": "https://google.com"
        }
    }

@patch("send_message_template.whatsapp_cloudapi.requests.post")
def test_send_message_with_text_media_and_button(mock_post, text_media_button_params):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    # Inject custom header_payload for test
    from send_message_template import whatsapp_cloudapi
    whatsapp_cloudapi.header_payload["image"] = "dummy/path/to/image.jpg"
    whatsapp_cloudapi.header_payload["buttons"] = [{
        "type": "url",
        "text": text_media_button_params["button"]["text"],
        "url": text_media_button_params["button"]["url"]
    }]

    sender = whatsapp_cloudapi.WhatsAppMessageSender(
        template_name=text_media_button_params["template_name"],
        template_params=text_media_button_params["template_params"]
    )

    response = sender.send_message_to_user()

    args, kwargs = mock_post.call_args
    payload = json.loads(kwargs['data'])

    # Check core structure
    assert payload["messaging_product"] == "whatsapp"
    assert payload["template"]["name"] == "test_template"

    # Header
    header_component = next(c for c in payload["template"]["components"] if c["type"] == "header")
    assert header_component["parameters"][0]["type"] == "image"
    assert "id" in header_component["parameters"][0]["image"]

    # Body
    body_component = next(c for c in payload["template"]["components"] if c["type"] == "body")
    assert body_component["parameters"][0]["text"] == "Check this out!"

    # Button
    button_component = next((c for c in payload["template"]["components"] if c["type"] == "button"), None)
    assert button_component is not None
    assert button_component["parameters"][0]["type"] == "text"
    assert button_component["parameters"][0]["text"] == text_media_button_params["button"]["url"]

    assert response.status_code == 200
    assert response.json() == {"success": True}
