from django.db import models
from Account.models import User
import uuid
from django.utils import timezone
# Create your models here.
class MyWallet(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username
    
class WalletHistory(models.Model):
    action=(('deposit','Deposit'),('Withdraw','Withdraw'),('Transfer','Transfer'),("pay","pay"))
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    wallet=models.ForeignKey(MyWallet,on_delete=models.CASCADE,related_name='owner')
    action=models.CharField(choices=action,max_length=50)
    amount=models.IntegerField()
    reciever=models.ForeignKey(MyWallet,on_delete=models.CASCADE,null=True,blank=True,related_name='receiver')
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.action