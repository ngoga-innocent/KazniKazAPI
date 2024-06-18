from .models import Room,Message
from django.db.models.signals import post_save

from django.dispatch import receiver
@receiver(post_save, sender=Message)
def update_last_message(sender,instance,created,**kwargs):
    if created:
        room=instance.room
        if instance.message_type=="message":
            room.last_message=instance.message
        elif instance.message_type=="image":
            room.last_message="Image Message"    
        elif instance.message_type=="video":
            room.last_message="Video Message"
            
        room.save()