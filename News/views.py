from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import New
from .serializer import NewSerializer
# Create your views here.
class NewsView(APIView):
    def get(self,request):
        news=New.objects.all()
        serializer=NewSerializer(news,many=True,context={"request":request})
        return Response({"news":serializer.data},status=200)