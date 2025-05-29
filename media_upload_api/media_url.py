#fetching media url by passing media id to the url

import requests

from settings import token, api_version
from media_upload_api.media_uploader import WhatsAppMediaUploader

media_id = WhatsAppMediaUploader().upload_media_to_server()

def get_media_url():
    url = f"https://graph.facebook.com/{api_version}/"#{media_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    image_url = response.json()
    return image_url

print(get_media_url())


def get_media_files_list():
    url = f"https://graph.facebook.com/{api_version}/{media_id}/media_file"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    media_files = response.json()
    return media_files

# print(get_media_files_list())

