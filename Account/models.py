from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class User(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    profile=models.ImageField(upload_to='Profile',null=True)
    phone_number=models.CharField(null=True,default='no provided number',blank=True,max_length=25)
    coverphoto=models.ImageField(upload_to='cover',null=True)
    seller=models.BooleanField(default=False)
    id_number=models.CharField(null=True,default='No number',max_length=16)
    id_card=models.ImageField(upload_to='ids',null=True)
    selfie=models.ImageField(upload_to='selfie',null=True)
    verified=models.BooleanField(default=False)

    REQUIRED_FIELDS=['email']