from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
#Registration View
class  Register(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"user":serializer.data},status=201)
        else:
            return Response({"detail":serializer.errors})
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
            return Response({"user":serializer.data})
        return Response({"detail":serializer.errors})


          