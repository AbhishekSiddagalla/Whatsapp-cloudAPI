# payload

from media_upload_api.media_uploader import WhatsAppMediaUploader

media_id = WhatsAppMediaUploader().upload_document_to_server()

header_payload = {
    "text": {
        "type": "text",
        "text": "default header text"
    },
    "image": {
        "type": "image",
        "image": {
            "id": media_id
        }
    },
    "video": {
        "type": "video",
        "video": {
            "id": media_id
        }
    },
    "document": {
        "type": "document",
        "document": {
            "id": media_id
        }
    }
}