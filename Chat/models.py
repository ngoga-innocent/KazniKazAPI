from django.db import models
from Account.models import User
import uuid
from django.utils import timezone
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.
class Room(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user1=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_1')
    user2=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_2')
    last_message=models.CharField(max_length=100000,null=True,blank=True)
    timestamp=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user1.username) + " and " + str(self.user2.username)
class Message(models.Model):
    message_choice=(
        ('text','text'),
        ('image','image'),
        ('audio','audio'),
        ('video','video'),
        ('file','file'),
        ('location','location'),
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    sender=models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
    message_type=models.CharField(max_length=500,default='text')
    message=models.CharField(max_length=100000,null=True,blank=True)
    image=models.ImageField(upload_to='Chat/Image',null=True,blank=True)
    video=models.FileField(upload_to='Chat/Video',storage=RawMediaCloudinaryStorage(resource_type='video'),null=True,blank=True)
    audio=models.FileField(upload_to='Chat/Audio',null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)  
    is_read=models.BooleanField(default=False)  

    def __str__(self):
        return str(self.message) + " and " + str(self.id)