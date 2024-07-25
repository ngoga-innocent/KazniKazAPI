from rest_framework import serializers
from Account.serializers import UserSerializer
from .models import MyWallet,WalletHistory
class MyWalletSerializer(serializers.ModelSerializer):
    user_details=UserSerializer(read_only=True,source='user')
    # user=UserSerializer(read_only=True)
    class Meta:
        model=MyWallet
        fields=['id','user','amount','user_details']
    
    

class WalletHistorySerializer(serializers.ModelSerializer):
    wallet_details=MyWalletSerializer(source='wallet',read_only=True)
    class Meta:
        model=WalletHistory
        fields=['id','action','amount','reciever','wallet','wallet_details','status','created_at']