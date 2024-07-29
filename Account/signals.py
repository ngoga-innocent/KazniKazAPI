from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Device,Notifications
from django.core.mail import send_mail
from django.conf import settings
from .firebase import send_push_notification
from Wallet.models import MyWallet
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        MyWallet.objects.create(user=instance)
        send_mail(
            f'Dear ' + instance.username +' Welcome to Kaz ni Kaz' ,
            'Thank you for registering on Kaz ni kaz.',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )

        notification=Notifications.objects.create(User=instance,notification_title="Registration Success", notification_body=f"Hello" +instance.username + " Your Account is Successfully Created",type="Self")
# @receiver(post_save,sender=Device)
# def send_message_notification(sender, instance,created,**kwargs):
#     if created:
#         print(instance.token)
#         send_push_notification(instance.token,f"Welcome" + instance.User.username +"  to Kaz ni Kaz!","Connect with The world Mobile!")
#         notification=Notifications.objects.create(User=instance,notification_title="Registration Success", notification_body=f"Hello" +instance.username + " Your Account is Successfully Created",type="Self")
       
#     send_push_notification(instance.token,f"Welcome Back" + instance.User.username +"  to Kaz ni Kaz!","Connect with The world Mobile!")    
