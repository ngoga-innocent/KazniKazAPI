from django.db import models
import uuid
from Account.models import User
# Create your models here.
class JobCategoryChoice(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.category
class Job(models.Model):
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    job_title=models.CharField(max_length=100)
    job_slug=models.CharField(max_length=255)
    job_description=models.TextField()
    job_thumbnail=models.ImageField(upload_to='JobThumb')
    job_location=models.CharField(max_length=100,null=True, blank=True)
    job_category=models.ManyToManyField(JobCategoryChoice, blank= False)
    job_provider=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title
