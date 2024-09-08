from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room,Message
from .serializer import RoomSerializer,MessageSerializer
from Account.models import User
from django.db.models import Q
import cloudinary.uploader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class RoomView(APIView):
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated,]  # Require authentication for POST
         # Allow any access for other methods
        return [permission() for permission in self.permission_classes]
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        rooms=Room.objects.filter(Q(user2=request.user)|Q(user1=request.user)).order_by('-timestamp')
        serializer=RoomSerializer(rooms,many=True,context={"request":request})
        return Response({"rooms":serializer.data},status=200)
    def delete(self,request,room_id):
        try:
            room=Room.objects.get(id=room_id)
            room.delete()
            return Response({"detail":"Room Deleted Successfully"},status=200)
        except Room.DoesNotExist:
            return Response({"detail":"Room Does not exist"},status=401)
    
class MessageView(APIView):
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated,]  # Require authentication for POST
         # Allow any access for other methods
        return [permission() for permission in self.permission_classes]
    def get(self, request,receiver_id):
       try:
           user2=User.objects.get(id=receiver_id)
           room=Room.objects.filter(Q(user1=request.user.id,user2=user2.id)| Q(user2=request.user.id,user1=user2.id)).first()
           if room is None:
               room=Room.objects.create(user1=request.user,user2=user2)
           messages=Message.objects.filter(room=room).order_by('timestamp')
           serializer=MessageSerializer(messages,many=True,context={"request":request})
           return Response({"messages":serializer.data},status=200)

       except User.DoesNotExist:
           return Response({"detail":"User Does not exist"},status=401)
    def post(self, request, receiver_id):
        try:
            user2 = User.objects.get(id=receiver_id)
            
            # Ensure user2 is not the same as the requesting user
            if user2 == request.user:
                return Response({"detail": "Cannot create a room with yourself."}, status=400)
            
            # Find or create the room
            room = Room.objects.filter(
                Q(user1=request.user, user2=user2) | Q(user1=user2, user2=request.user)
            ).first()
            if not room:
                room = Room.objects.create(user1=request.user,user2=user2)
            
            serializer = MessageSerializer(
                data=request.data, 
                context={'sender': request.user, 'receiver': user2, "room": room}
            )
            
            if serializer.is_valid():
                chat=serializer.save()
                if chat.message_type == 'video':
                    pass
                return Response({"message": serializer.data}, status=201)
            else:
                return Response({"detail": serializer.errors}, status=400)
        
        except User.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=400) 
    def delete(self, request,receiver_id):
        try:
            message=Message.objects.get(id=receiver_id)
            message.delete()
            return Response({"detail":"Message Deleted Successfully"},status=200)
        except Message.DoesNotExist:
            return Response({"detail":"Message Does not exist"},status=401)    
    def put(self,request,receiver_id):
        try:
           
            message=Message.objects.get(id=receiver_id)
            message.is_read=True
            message.save()
            return Response({"detail":"Message Saved Successfully"},status=200)  
        except Message.DoesNotExist:
            return Response({"detail":"Message Does not exist"},status=401)


              

