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
    def post(self, request):
        serializer = NewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"news": serializer.data}, status=201)
        return Response({"detail": serializer.errors}, status=400)
    def put(self,request,news_id):
        try:
            news=New.objects.get(id=news_id)
            serializer=NewSerializer(news,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"news":serializer.data},status=200)
            else:
                return Response({"detail":serializer.errors},status=401)
        except New.DoesNotExist:
            return Response({"detail":"News Does not exist"},status=401)
    def delete(self, request,news_id):    
        try:
            news=New.objects.get(id=news_id)
            news.delete()
            return Response({"detail":"News Deleted Successfully"},status=200)
        except New.DoesNotExist:
            return Response({"detail":"News Does not exist"},status=401)
       