#fetching media id by uploading media to the server
import os
import requests

from settings import api_version, phone_number_id, token, media_file_path, app_id,fb_app_access_token


class WhatsAppMediaUploader:
    def __init__(self):
        self.api_version = api_version
        self.phone_number_id = phone_number_id
        self.token = token
        self.app_id = app_id
        self.fb_app_access_token = fb_app_access_token
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/media"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }

    def upload_document_to_server(self):
        headers = self._get_headers()

        data = {
            "messaging_product": "whatsapp",
        }
        with open(media_file_path, 'rb') as media_file:
            files = {
                'file': ('order.png', media_file,'image/png')
            }
            response = requests.post(self.base_url, headers=headers, files=files, data=data).json()
            return response.get("id")

class WhatsAppMediaUploadSession:
    def __init__(self):
        self.api_version = api_version
        self.app_id = app_id
        self.token = token
        self.file_name = media_file_path
        self.file_length = os.path.getsize(media_file_path)
        self.file_type = "image/jpg"
        self.base_url = f"https://graph.facebook.com/{api_version}/{self.app_id}/uploads?file_name={self.file_name}&file_length={self.file_length}&file_type={self.file_type}&access_token={self.token}"

    def generate_session_id(self):
        response = requests.post(self.base_url).json().get("id")
        return response

upload_session = WhatsAppMediaUploadSession()
session_id = upload_session.generate_session_id()

class HeaderHandle:
    def __init__(self):
        self.session_id = session_id
        self.fb_app_access_token = fb_app_access_token
        self.file_name = media_file_path
        self.session_url = f"https://graph.facebook.com/v22.0/{session_id}"

    @staticmethod
    def _get_headers(self):
        return {
            "Authorization": f"OAuth {token}",
            "file_offset": "0"
        }
    def get_header_handle(self):
        headers = self._get_headers()
        with open(self.file_name, 'rb') as media_file:
            files = {
                'file': ('order.png', media_file,'image/png')
            }
            response = requests.post(self.session_url, headers=headers, files=files).json().get("h")
            return response






