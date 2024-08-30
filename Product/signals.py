from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductModel,ShopModel
from Account.models import Device,Notifications
from django.conf import settings
from Account.firebase import send_push_notification
from Account.serializers import NotificationSerializer
@receiver(post_save, sender=ProductModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        if instance.shop:
            try:
                device=Device.objects.get(User=instance.shop.owner)
                send_push_notification(device.token,f"" +instance.name +" Uploaded to Kaz ni Kaz!","Your Product has been Successfully Uploaded!")
            except Device.DoesNotExist:  
                pass      
        elif instance.uploader:
            try:
                device=Device.objects.get(User=instance.uploader)
                send_push_notification(device.token,f"" +instance.name +" Uploaded to Kaz ni Kaz!","Your Product has been Successfully Uploaded!")
            except Device.DoesNotExist:  
                pass              
        if instance.discount:
            alldevice =Device.objects.all()
            for device in alldevice:
                send_push_notification(device.token,f"New Product " +instance.name +"  to Kaz ni Kaz!","Don't Miss This New Product!")
               

@receiver(post_save,sender=ShopModel)
def send_message_notification(sender, instance,created,**kwargs):
    if created:
        try:
            device=Device.objects.get(User=instance.owner)
            notifiction_data={
                'notification_title': f" Your" +instance.name + " has been created",
                'notification_body': f"Your Shop" +instance.name + " has been created, Welcome to Worldwide Market",
                'type': 'Self',
                
            }
            notification=NotificationSerializer(data=notifiction_data)
            if notification.is_valid():
                notification.save()
            send_push_notification(device.token,f"New Shop " +instance.name +"  to Kaz ni Kaz!","Hurry Up to publicize your Products!")
        except Device.DoesNotExist:
            pass    
        devices=Device.objects.filter(User=instance.owner)
        for device in devices:

            send_push_notification(device.token,f"New Shop" +instance.name + f"to Kaz ni Kaz!","Browser and Follow This shop to get Notified on new" +instance.name + "Product!")
       
