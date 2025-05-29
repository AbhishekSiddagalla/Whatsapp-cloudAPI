# payload

from media_upload_api.media_uploader import WhatsAppMediaUploader

media_id = WhatsAppMediaUploader().upload_media_to_server()

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
#button payload
buttons_payload = {
    "phone_number": {
        "type": "PHONE_NUMBER",
        "text": "Phone Number",
        "phone_number": str(input("Enter Phone Number to add in the message button:"))
    },
    "url": {
        "type": "URL",
        "text": "Website",
        "url": str(input("Enter URL to add in the message button:"))
    }
}