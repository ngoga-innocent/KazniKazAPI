from django.db import models
from Account.models import User
import uuid
from django.utils import timezone
# Create your models here.
class MyWallet(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    amount=models.IntegerField(default=10000)

    def __str__(self) -> str:
        return self.user.username
    
class WalletHistory(models.Model):
    action=(('deposit','Deposit'),('Withdraw','Withdraw'),('Transfer','Transfer'),("pay","pay"))
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    wallet=models.ForeignKey(MyWallet,on_delete=models.CASCADE,related_name='owner')
    action=models.CharField(choices=action,max_length=50)
    amount=models.IntegerField()
    status=models.CharField(max_length=255,default="pending")
    payment_ref=models.CharField(max_length=500,null=True)
    reciever=models.ForeignKey(MyWallet,on_delete=models.CASCADE,null=True,blank=True,related_name='receiver')
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} order from {self.created_at}"
class Payments(models.Model):
    action=(('Deposit','Deposit'),('Withdraw','Withdraw'),('Transfer','Transfer'),("pay","pay"))
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) 
    referenceKey=models.CharField(max_length=255,null=False,blank=False)
    number=models.CharField(max_length=255,null=False)
    amount=models.IntegerField(null=False)
    payer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    action=models.CharField(choices=action,max_length=255,default='pay')
    status=models.CharField(max_length=255,null=False)
    created_at=models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"reference key {self.referenceKey} created at {self.created_at}"