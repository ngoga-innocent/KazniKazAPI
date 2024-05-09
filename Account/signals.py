from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'Dear ' + instance.username +' Welcome to Kaz ni Kaz' ,
            'Thank you for registering on Kaz ni kaz.',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )