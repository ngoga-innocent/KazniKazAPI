from rest_framework import serializers

from .models import User,Device,Notifications
from django.contrib.auth.password_validation import validate_password
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     class Meta:
#         model=User
#         fields = ['id','username', 'email','phone_number', 'password', 'profile', 'coverphoto', 'id_card', 'selfie', 'seller', 'verified']
#         extra_kwargs = {
#             'profile': {'required': False},
#             'coverphoto': {'required': False},
#             'id_card': {'required': False},
#             'selfie': {'required': False},
#             'seller': {'required': False},
#             'verified': {'read_only': True}
#         }
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             profile=validated_data.get('profile'),
#             coverphoto=validated_data.get('coverphoto'),
#             id_card=validated_data.get('id_card'),
#             selfie=validated_data.get('selfie'),
#             seller=validated_data.get('seller', False),

            
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone_number', 'password', 'profile','id_number', 
            'coverphoto', 'id_card', 'selfie', 'seller', 'verified', 'account_status'
        ]
        extra_kwargs = {
            'profile': {'required': False},
            'coverphoto': {'required': False},
            'id_card': {'required': False},
            'selfie': {'required': False},
            'seller': {'required': False},
            'verified': {'read_only': True},
            'account_status': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            profile=validated_data.get('profile'),
            coverphoto=validated_data.get('coverphoto'),
            id_card=validated_data.get('id_card'),
            selfie=validated_data.get('selfie'),
            seller=validated_data.get('seller', False),
            account_status=validated_data.get('account_status', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        User=UserSerializer(read_only=True,required=False)
        model=Device 
        fields=['token','User']   

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        User=UserSerializer(read_only=True,required=False)
        model=Notifications
        fields='__all__'        