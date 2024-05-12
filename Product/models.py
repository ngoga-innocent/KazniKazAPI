from django.db import models
import uuid
from Account.models import User
from django.utils import timezone
# Create your models here.

class ShopModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    name=models.CharField(max_length=255,null=False)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='shop_owner')
    thumbnail=models.ImageField(upload_to='Shop_thumbnail')
    location=models.CharField(max_length=255)
    contact=models.CharField(max_length=255,null=True)
    like=models.IntegerField()
    followers=models.IntegerField()
    
    def __str__(self):
        return self.name
class Colors(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    color=models.CharField(max_length=255)

    def __str__(self):
        return self.color
class Category(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255)
    thumbnail=models.ImageField(upload_to='Category_thumbnails')
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
class ProductModel(models.Model):

    choice=(("Normal","Normal"),("Vip","Vip"))
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255)
    description=models.TextField()
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE,null=True)
    price=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to='product_thumbnail')
    uploader=models.ForeignKey(User,on_delete=models.CASCADE,related_name='uploader')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default='Other')
    colors=models.ManyToManyField(Colors,related_name='product_colours')
    discount=models.IntegerField(null=True)
    place=models.CharField(choices=choice,max_length=255,default='Normal')
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
class ProductImage(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='product_images')
    image=models.ImageField(upload_to='Image_pictures')
    
    
class Like(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    liker=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liker')
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE,related_name='shop_liked')
class Comment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)  
    commenter=models.ForeignKey(User,on_delete=models.CASCADE)
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE)