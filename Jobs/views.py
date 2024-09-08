from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job, JobCategoryChoice
from .serializer import JobSerializer, JobCategorySerializer

# Create your views here.

class JobView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT':
            self.permission_classes = [IsAuthenticated]    
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True, context={"request": request})
        return Response({"jobs": serializer.data}, status=200)

    def post(self, request):
        serializer = JobSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"job": serializer.data}, status=201)
        return Response({"detail": serializer.errors}, status=400)

    def put(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"job": serializer.data}, status=200)
            return Response({"detail": serializer.errors}, status=400)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found"}, status=404)
    def delete(self,request,job_id):
        try:
            job=Job.objects.get(id=job_id)
            job.delete()
            return Response({"detail":"Job Deleted Successfully"},status=200)
        except Job.DoesNotExist:
            return Response({"detail":"Job Does not exist"},status=401)    
           

class JobCategoryViews(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        job_categories = JobCategoryChoice.objects.all()
        serializer = JobCategorySerializer(job_categories, many=True)
        return Response({"job_categories": serializer.data}, status=200)
