from .models import Job,JobCategoryChoice
from rest_framework import serializers
from Account.serializers import UserSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    job_provider=UserSerializer(read_only=True)
    class Meta:
        model=JobCategoryChoice
        fields='__all__'
class JobSerializer(serializers.ModelSerializer):
    job_provider=UserSerializer(read_only=True)
    job_category = JobCategorySerializer(many=True, read_only=True)
    class Meta:
        model=Job
        fields='__all__'
    def create(self, validated_data):
        validated_data['job_provider']=self.context['user']
        return Job.objects.create(**validated_data)
    