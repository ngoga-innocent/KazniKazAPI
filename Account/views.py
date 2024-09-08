from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Device,Notifications,OTP
from .serializers import UserSerializer,DeviceSerializer,NotificationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.views import View
from django.shortcuts import render,redirect
from django.db.models import Q
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Registration View
class  Register(APIView):
    def post(self, request):
        # Extract data from request
        device_token = request.data.get('device_token')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        print(request.data)
        # Check if the email is already used
        if email and User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            return Response({"detail": f"Email already used by {username}"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the phone number is already used
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            username = User.objects.get(phone_number=phone_number).username
            return Response({"detail": f"Phone number already used by {username}"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the new user data
        serializer = UserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()

            # Handle device token if provided
            if device_token:
                try:
                    device = Device.objects.get(token=device_token)
                    device.User = user  # Ensure to use the correct attribute name 'user'
                    device.save()
                except Device.DoesNotExist:
                    # Create a new Device instance if it does not exist
                    Device.objects.create(token=device_token, user=user)
                except Exception as e:
                    # Handle any unexpected exceptions and return an appropriate response
                    return Response({"detail": f"An error occurred while handling the device token: {str(e)}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Return the first error message
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({"detail": first_error}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure a response is returned in all cases
        return Response({"detail": "An unknown error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                return Response({"detail":'User with this email  not found please consider using username'},status=401) 
        else:
            try:
                user=User.objects.get(Q(username=username.capitalize())|Q(phone_number=username))
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
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        user=request.user
        serializer=UserSerializer(user)
        return Response({"user":serializer.data})
    def put(self,request):
        user=request.user
        id_Number=request.data.get("id_number")
        if id_Number:
            find_idnumber=User.objects.filter(id_Number=id_Number).first()
            if find_idnumber and find_idnumber.verified:
                return Response({"detail":f"Id Number already Verified by" +find_idnumber.username})
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
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        five_days=timezone.now() - timedelta(days=5)
        # print(five_days)
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
def request_verification(request):
    user=request.user
    if user:
        serializer=UserSerializer(user,request.POST,partial=True,context={"request":request})   
        if serializer.is_valid():
            user=serializer.save()
            user.account_status="Pending"
            user.save()
            return Response({"user":serializer.data},status=200)
        else:
            return Response({"detail":serializer.data},status=401)
    else:
        return Response({"detail":"Pleease Login First"},status=400)      
class GenerateOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist.","success":False}, status=200)

        # Generate a 6-digit random OTP
        otp_code = str(random.randint(100000, 999999))

        # Create or update OTP for the user
        otp, created = OTP.objects.get_or_create(user=user)
        otp.otp_code = otp_code
        otp.created_at = timezone.now()
        otp.is_used = False
        otp.save()
        context = {
            'user': user,
            'otp': otp_code,
        }
        html_content = render_to_string('EmailTemplates/password_reset.html', context)
        text_content = strip_tags(html_content)
        # Send OTP via email (you could also use SMS here)
        email = EmailMultiAlternatives(
            subject='Your OTP Code for Password Reset',
            body=text_content,
            from_email='kaznikaz@gmail.com',
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"detail": "OTP sent to your email.","success":True}, status=200)

class checkOtp(APIView):
    def post(self,request):
        otp=request.data.get('otp')
        try:
            otp_obj=OTP.objects.get(otp_code=otp)
            print(otp_obj)
            if not otp_obj.is_valid():
                return Response({"detail":"OTP has been expired","success":False},status=200)
        except OTP.DoesNotExist:
            return Response({"detail":"invalid Otp","success":False},status=200)
        return Response({"detail":"otp validated","success":True},status=200)    
        
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

class ResetPasswordView(APIView):
    

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.get(user=user, otp_code=otp_code)
            except (User.DoesNotExist, OTP.DoesNotExist):
                print("Invalid Otp or Email")
                return Response({"detail": "Invalid OTP or email.","success":False}, status=200)

            # Check if OTP is valid
            if not otp.is_valid():
                print("invalid otp")
                return Response({"detail": "OTP has expired or is already used.","success":False}, status=200)

            # Reset password
            user.set_password(new_password)
            user.save()

            # Mark OTP as used
            otp.is_used = True
            otp.save()
            otp.delete()

            return Response({"detail": "Password reset successful.","success":True}, status=200)
        else:
            print(serializer.errors)
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({"detail":first_error,"success":False}, status=400)   
     

