import firebase_admin
from firebase_admin import credentials, messaging
import os
# Path to your service account key file
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'firebasefile.json'))
cred = credentials.Certificate(json_path)


# Initialize the app with a service account, granting admin privileges
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

    response = messaging.send(message)
    print(response)
    return response