from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import datetime
# Create your models here.
class User(AbstractUser):
    def create_user(self, **extra_fields):
        
        if username:
            username = username.capitalize()  # Capitalize the username
        user = self.model(username=username, **extra_fields)
        
        user.save(using=self._db)
        return user
    status_choice=(
        ("Not_Verified","Not Verified"),
        ("Pending","Pending"),
        ("Verified","Verified"),
        ("Rejected","Rejected"),
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=True,blank=True,unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile=models.ImageField(upload_to='Profile',null=True,blank=True)
    
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
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)  # OTP can be a 6-digit code
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Check if the OTP is valid (e.g., not expired and not used)
        now = timezone.now()
        expiration_time = self.created_at + datetime.timedelta(minutes=10)  # OTP valid for 10 minutes
        return now <= expiration_time and not self.is_used        