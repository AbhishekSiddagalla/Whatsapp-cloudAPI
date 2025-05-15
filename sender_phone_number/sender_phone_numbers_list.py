import requests

from settings import api_version, whatsapp_business_account_id, token

# fetching all sender's phone numbers
def get_phone_numbers_list():
    url = f"https://graph.facebook.com/{api_version}/{whatsapp_business_account_id}/phone_numbers?access_token={token}"
    response = requests.get(url)
    phone_numbers = response.json()
    return phone_numbers["data"][0]["id"]

phone_number_id = get_phone_numbers_list()
