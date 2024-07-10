import firebase_admin
from firebase_admin import credentials, messaging
import os
# Path to your service account key file
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'firebase_setting.json'))
cred = credentials.Certificate(json_path)


# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)
from django.http import HttpResponse
from .models import Device
def send_push_notification(token, title, body):
    print(json_path)
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