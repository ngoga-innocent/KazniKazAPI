from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from Account.firebase import send_push_notification
from Account.models import Device,Notifications
from Account.serializers import NotificationSerializer
@receiver(post_save,sender=Job)
def notifyUser(sender,instance,created,**kwargs):
    if created:
        notification_data={
            "notification_title":"New Job Posted",
            "notification_body":f"New Job" +instance.job_title + " just posted Check on kaz ni Kaz Now ",
            "type":"App",
            
            
            
        }
        notification=NotificationSerializer(data=notification_data)
        if notification.is_valid():
            notification.save()
        else:
            print(notification.errors)    
        # notification=Notifications.objects.create(User=instance.job_provider,notification_title="New Job Posted", notification_body=f"New Job" +instance.name + " just posted ",type="App")
        devices=Device.objects.all()
        for device in devices:
            send_push_notification(device.token,f'New Job Posted: {instance.job_title}',f" Posted By:" + instance.job_provider.username)