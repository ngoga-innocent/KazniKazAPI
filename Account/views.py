from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Device,Notifications
from .serializers import UserSerializer,DeviceSerializer,NotificationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.views import View
from django.shortcuts import render
#Registration View
class  Register(APIView):
    def post(self,request):
        device_token=request.data.get('device_token')
        
        serializer=UserSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            user=serializer.save()
            if device_token is not None:
                try:
                    device=Device.objects.get(token=device_token)
                    device.User=user
                    device.save()
                except Device.DoesNotExist:
                    device=Device.objects.create(token=device_token,User=user)    
                return Response({"user":serializer.data},status=201)
        else:
            return Response({"detail":serializer.errors},status=500)
class Login(APIView):
    def post(self,request):
        username=request.data['username']
      
        password=request.data['password']

        if '@' in username:
            
            try:
                user=User.objects.get(email=username)
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    serializer=UserSerializer(user)
                    

                    return Response({"user":serializer.data,"token":token.key})
                else:
                    return Response({"detail":"incorrect password"},status=401)

            except User.DoesNotExist:
                return Response({"detail":'User with this username not found'},status=401) 
        else:
            try:
                user=User.objects.get(username=username)
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    serializer=UserSerializer(user)
                    

                    return Response({"user":serializer.data,"token":token.key})
                else:
                    return Response({"detail":"incorrect password"},status=401)

            except User.DoesNotExist:
                return Response({"detail":'User with this username not found'},status=401)
class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        user=request.user
        serializer=UserSerializer(user)
        return Response({"user":serializer.data})
    def put(self,request):
        user=request.user
        serializer=UserSerializer(user,data=request.data,partial=True,context={"request":request})
        if serializer.is_valid():

            serializer.save()
            notification_data={
                "notification_title":"Your Profile has been updated",
                "notification_body":"Your profile has been updated Successfully",
                "User":user.id,
                "type":"Self"
            }
            notification_serializer=NotificationSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save()
            else:
                print(notification_serializer.errors)    
            return Response({"user":serializer.data},status=200)
        return Response({"detail":serializer.errors})


class DeviceRegister(APIView):
    def post(self, request, *args, **kwargs):
        token=request.data.get('token')
        check_token=Device.objects.filter(token=token).exists()
        if not check_token:
            serializer = DeviceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"device": serializer.data}, status=201)
            return Response({"detail": serializer.errors}, status=400)
class NotificationView(APIView):
    def get(self, request):
        five_days=timezone.now() - timedelta(days=5)
        print(five_days)
        if request.user.is_authenticated:
            notifications=Notifications.objects.filter(Q(User=request.user) | Q(type='App'), is_read=False)
        notifications=Notifications.objects.filter(type='App', is_read=False,timestamp__gte=five_days)
        serializer=NotificationSerializer(notifications,many=True)
        return Response({"notifications":serializer.data})
    def put(self, request):
        notification_id=request.data.get('notification_id')
        notification=Notifications.objects.get(id=notification_id)
        notification.is_read=True
        notification.save()
        return Response({"detail":"Notification Marked As Read"})
class WebSignup(View):
    def get(self, request):
        return render(request, 'signup.html')    

