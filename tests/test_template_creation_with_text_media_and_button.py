import pytest
import json
from unittest.mock import patch, MagicMock
from message_template_creation.whatsapp_cloudapi_template_creation import MessageTemplateCreator


@pytest.fixture
def valid_template_payload():
    return {
        "name": "test_template",
        "header_format": "IMAGE",
        "header_text": None,
        "body_text": "Welcome, {{1}}!",
        "footer_text": "Thank you!",
        "buttons": [
            {"type": "URL", "text": "Visit", "url": "https://google.com"},
            {"type": "PHONE_NUMBER", "text": "Call Us", "phone_number": "+1234567890"}
        ],
        "body_example_params": [["John"]]
    }

@patch("message_template_creation.whatsapp_cloudapi_template_creation.requests.post")
@patch("media_upload_api.media_uploader.HeaderHandle")
def test_create_template_with_valid_payload(mock_header_handle_class, mock_post, valid_template_payload):
    mock_header_handle = MagicMock()
    mock_header_handle.get_header_handle.return_value = "mock_media_id"
    mock_header_handle_class.return_value = mock_header_handle

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_post.return_value = mock_response

    creator = MessageTemplateCreator()
    response = creator.create_template_with_payload(**valid_template_payload)

    assert response == {"success": True}
    assert mock_post.called
    payload = json.loads(mock_post.call_args[1]["data"])
    assert payload["name"] == "test_template"
    assert payload["category"] == "UTILITY"
    assert payload["language"] == "en_US"
    assert any(comp["type"] == "HEADER" for comp in payload["components"])
    assert any(comp["type"] == "BODY" for comp in payload["components"])
    assert any(comp["type"] == "FOOTER" for comp in payload["components"])
    assert any(comp["type"] == "BUTTONS" for comp in payload["components"])


@patch("message_template_creation.whatsapp_cloudapi_template_creation.requests.post")
@patch("media_upload_api.media_uploader.HeaderHandle")
def test_create_template_without_optional_fields(mock_header_handle_class, mock_post):
    mock_header_handle = MagicMock()
    mock_header_handle.get_header_handle.return_value = "mock_media_id"
    mock_header_handle_class.return_value = mock_header_handle

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_post.return_value = mock_response

    creator = MessageTemplateCreator()
    response = creator.create_template_with_payload(
        name="no_optional",
        header_format=None,
        header_text=None,
        body_text="Just a body",
        footer_text=None,
        buttons=None,
        body_example_params=None
    )

    assert response == {"success": True}
    payload = json.loads(mock_post.call_args[1]["data"])
    assert len(payload["components"]) == 1  # Only BODY


@patch("message_template_creation.whatsapp_cloudapi_template_creation.requests.post")
@patch("media_upload_api.media_uploader.HeaderHandle")
def test_create_template_with_invalid_media_id(mock_header_handle_class, mock_post):
    mock_header_handle = MagicMock()
    mock_header_handle.get_header_handle.return_value = None
    mock_header_handle_class.return_value = mock_header_handle

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Invalid media ID"}
    mock_post.return_value = mock_response

    creator = MessageTemplateCreator()
    response = creator.create_template_with_payload(
        name="invalid_media",
        header_format="IMAGE",
        header_text=None,
        body_text="Body",
        footer_text=None,
        buttons=None,
        body_example_params=None
    )

    assert response["error"] == "Invalid media ID"


@patch("message_template_creation.whatsapp_cloudapi_template_creation.requests.post")
@patch("media_upload_api.media_uploader.HeaderHandle")
def test_create_template_with_invalid_button_data(mock_header_handle_class, mock_post):
    mock_header_handle = MagicMock()
    mock_header_handle.get_header_handle.return_value = "mock_media_id"
    mock_header_handle_class.return_value = mock_header_handle

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "error": {
            "message": "Invalid button format.",
            "code": 100
        }
    }
    mock_post.return_value = mock_response

    creator = MessageTemplateCreator()
    response = creator.create_template_with_payload(
        name="invalid_button",
        header_format="IMAGE",
        header_text=None,
        body_text="Test",
        footer_text=None,
        buttons=[{"type": "WRONG", "text": None}],
        body_example_params=None
    )

    assert "error" in response
    assert response["error"]["message"] == "Invalid button format."
