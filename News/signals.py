from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import New
from Account.models import Device
from Account.firebase import send_push_notification
@receiver(post_save,sender=New)
def Send_update_News(sender,instance,created,**kwargs):
    if created:
        devices =Device.objects.all()
        for device in devices: send_push_notification(device.token,instance.title,f"Hot News"+instance.link)