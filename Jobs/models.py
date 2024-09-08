from django.db import models
import uuid
from Account.models import User
import datetime
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class JobCategoryChoice(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.category
class Job(models.Model):
    currency=(
        ("Rwf","Rwf"),
        ("USD","USD")
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    job_title=models.CharField(max_length=100)
    job_slug=models.CharField(max_length=255)
    job_description=models.TextField()
    job_thumbnail=models.ImageField(upload_to='JobThumb')
    job_location=models.CharField(max_length=100,null=True, blank=True)
    job_category=models.ForeignKey(JobCategoryChoice, blank= True,null=True, on_delete=models.SET_NULL)
    job_provider=models.ForeignKey(User,on_delete=models.CASCADE)
    job_contact=models.CharField(max_length=255,null=True,blank=True)
    company=models.CharField(max_length=255,null=True,blank=True)
    job_open=models.BooleanField(default=True)
    job_min_salary=models.IntegerField(default=10000)
    job_max_salary=models.IntegerField(default=50000)
    currency=models.CharField(max_length=10,choices=currency,default="Rwf")
    created_at=models.DateField(default=timezone.now)
    
    def default_deadline():
        return timezone.now() + timedelta(days=30)
    
    job_deadline = models.DateField(default=default_deadline)
    def __str__(self):
        return self.job_title
    def check_deadline(self):
        """Check if the job deadline has passed and close the job if necessary."""
        if self.job_deadline < timezone.now().date() and self.job_open:
            self.job_open = False
            self.save()
        return self.job_open