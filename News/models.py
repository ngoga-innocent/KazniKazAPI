from django.db import models
import uuid
# Create your models here.
class New(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=100)
    link=models.TextField()
    thumbbail=models.ImageField(upload_to='News')
    
    def __str__(self):
        return self.title