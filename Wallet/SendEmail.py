from django.core.mail import send_mail
from django.conf import settings
def sending_email(sender,title,message):
    
        send_mail(
            title,
            message,
            settings.EMAIL_HOST_USER,
            [sender.email],
            fail_silently=False,
        )