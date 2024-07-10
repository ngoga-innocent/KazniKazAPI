import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.http import HttpResponse
from .models import Device
# Path to your service account key file
# json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'firebase_setting.json'))
# cred = credentials.Certificate(json_path)

FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n')
PRIVATE_KEY_ID = os.getenv('PRIVATE_ID')
FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI')
FIREBASE_AUTH_PROVIDER_CERT_URL = os.getenv('FIREBASE_AUTH_PROVIDER_CERT_URL')
FIREBASE_CLIENT_CERT_URL = os.getenv('FIREBASE_CLIENT_CERT_URL')
FIREBASE_UNIVERSE_DOMAIN = os.getenv('FIREBASE_UNIVERSE_DOMAIN')

# Initialize Firebase with your service account credentials
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": FIREBASE_PROJECT_ID,
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": FIREBASE_PRIVATE_KEY,
    "client_email": FIREBASE_CLIENT_EMAIL,
    "client_id": FIREBASE_CLIENT_ID,
    "auth_uri": FIREBASE_AUTH_URI,
    "token_uri": FIREBASE_TOKEN_URI,
    "auth_provider_x509_cert_url": FIREBASE_AUTH_PROVIDER_CERT_URL,
    "client_x509_cert_url": FIREBASE_CLIENT_CERT_URL,
    "universe_domain": FIREBASE_UNIVERSE_DOMAIN
})
firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body):
   
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
                "url": 'KazniKaz://logins'
            },
        token=token,
    )
    try:
        messaging.send(message)
        print("Successfully sent message:", token)
    except firebase_admin._messaging_utils.UnregisteredError:
        print("Failed to send",token)
        # Handle the unregistered token here, e.g., remove it from your database
        Device.objects.filter(token=token).delete()
        return None    
    return True