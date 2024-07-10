from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class New(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=100)
    
    link=models.TextField()
    thumbnail=models.ImageField(upload_to='News')
    created_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title