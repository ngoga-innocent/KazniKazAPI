from rest_framework import serializers
from .models import Room,Message
from Account.serializers import UserSerializer
class RoomSerializer(serializers.ModelSerializer):
    user1=UserSerializer(read_only=True)
    user2=UserSerializer(read_only=True)
    class Meta:
        model=Room
        fields=['id','user1','user2']
class MessageSerializer(serializers.ModelSerializer):
    sender=UserSerializer(read_only=True)
    receiver=UserSerializer(read_only=True)
    room=RoomSerializer(read_only=True)
    class Meta:
        model=Message
        fields=['id','room','sender','receiver','message_type','message','image','video','audio','timestamp']

    def create(self,validated_data):
        validated_data['sender'] = self.context['sender']
        validated_data['receiver'] = self.context['receiver']
        validated_data['room'] = self.context['room']
        return Message.objects.create(**validated_data)          

