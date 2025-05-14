#fetching media id by uploading media to the server
import requests

from settings import api_version, phone_number_id, token, media_file_path,app_id

def upload_image_to_server():
    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/media"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "messaging_product": "whatsapp"
    }

    with open(media_file_path, 'rb') as img_file:
        files = {
            'file': ('image.png', img_file, 'image/png')
        }

        response = requests.post(url, headers=headers, files=files, data=data)
    return response.json().get("id")


def generate_image_session_id():
    url = f"https://graph.facebook.com/{api_version}/{app_id}/uploads"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "file_name": media_file_path,
        "file_length": 5961,
        "file_type": "image/png",
        "access_token": token
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()['id']

def create_handle():
    session_id = generate_image_session_id()

    url = f"https://graph.facebook.com/{api_version}/upload:{session_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "file_offset": "0"
    }
    response = requests.post(url, headers=headers)
    print(response.json())

create_handle()