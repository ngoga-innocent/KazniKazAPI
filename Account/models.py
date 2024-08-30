from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
# Create your models here.
class User(AbstractUser):
    status_choice=(
        ("Not_Verified","Not Verified"),
        ("Pending","Pending"),
        ("Verified","Verified"),
        ("Rejected","Rejected"),
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    profile=models.ImageField(upload_to='Profile',null=True,blank=True)
    phone_number=models.CharField(null=True,blank=True,max_length=25)
    coverphoto=models.ImageField(upload_to='cover',null=True)
    seller=models.BooleanField(default=False)
    id_number=models.CharField(null=True,blank=True,default='No number',max_length=16)
    id_card=models.ImageField(upload_to='ids',null=True,blank=True)
    selfie=models.ImageField(upload_to='selfie',null=True,blank=True)
    signup_type = models.CharField(max_length=50, null=False, blank=False,default="none")
    account_status=models.CharField(max_length=255,default="Not_Verified",choices=status_choice)
    verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=timezone.now)
    

    REQUIRED_FIELDS=['email']

class Device(models.Model):
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    token=models.CharField(max_length=1000,null=True)   

    def __str__(self):
        return str(self.User)
    
class Notifications(models.Model):
    choices=(
        ("App", "App"),
        ("Self","Self"),
        
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    notification_title=models.CharField(max_length=255,null=True)
    notification_body=models.CharField(max_length=1000)
    timestamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    type=models.CharField(max_length=50,choices=choices)
    def __str__(self):    
        return self.notification_title
    class Meta:
        
        verbose_name = 'Notifcation'
        verbose_name_plural = 'Notifcations'