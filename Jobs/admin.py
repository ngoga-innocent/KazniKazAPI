from django.contrib import admin
from .models import Job,JobCategoryChoice
# Register your models here.
admin.site.register(Job)
admin.site.register(JobCategoryChoice)