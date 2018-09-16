from oauth2client.service_account import ServiceAccountCredentials
import base64
import time

GB_SERVICE_KEY = '6dbb667caaaa5a453a21f77e2a67a5b698d11815'
GB_EMAIL_KEY = 'databaseuser@bumblebee-mit.iam.gserviceaccount.com'


def sign_url(file):
    epoch = int(time.time() + 10000)
    signed_string = 'GET\n' + epoch + "\n/bumblebee-audiofiles/snippets/" + file
    creds = ServiceAccountCredentials.from_json_keyfile_name(['service.json'])
    client_id = creds.service_account_email
    signature = creds.sign_blob([signed_string])[1]
    encoded_signature = base64.b64encode(signature)
    encoded_signature = encoded_signature.replace("/", "%2F").replace("+", "%2B") 
    base_url = 'https://storage.googleapis.com/bumblebee-audiofiles/snippets/' + file
    final_url = base_url + "?GoogleAccessId=" + client_id + "&Expires=" + epoch + "&Signature=" + encoded_signature
    return final_url

