from django.db import models
import uuid
from Account.models import User
from django.utils import timezone
# Create your models here.
class ShopCategory(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    name=models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.name
    
class ShopModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    name=models.CharField(max_length=255,null=False)
    shop_category=models.ForeignKey(ShopCategory,on_delete=models.CASCADE,null=True,blank=True)
    slug=models.CharField(max_length=255,null=True,blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='shop_owner')
    verified=models.BooleanField(default=False)
    thumbnail=models.ImageField(upload_to='Shop_thumbnail',null=True,blank=True)
    location=models.CharField(max_length=255)
    contact=models.CharField(max_length=255,null=True)
    like=models.IntegerField(default=0)
    followers=models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='Shops'
    def shop_products(self):
        return self.productmodel_set.all()    
class Colors(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    color=models.CharField(max_length=255)

    def __str__(self):
        return self.color
class Category(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255)
    thumbnail=models.ImageField(upload_to='Category_thumbnails')
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='Categories'
    def getCategoryChildren(self):
        return Category.objects.filter(parent=self)   
    def getProductCategory(self):
        return self.productmodel_set.all()
    def getCategorythreeProducts(self):
        return self.productmodel_set.all()[:3] 
    def getCategoryFeatures(self):
        return CategoryFeatures.objects.filter(category=self)
class CategoryFeatures(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_features')

    def __str__(self):
        return self.name + " " + self.category.name
    def featureOptions(self):
        return FeatureOptions.objects.filter(feature=self)
    class Meta:
        verbose_name = 'Features of Category'
        verbose_name_plural = 'Features of Category'
class FeatureOptions(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    feature=models.ForeignKey(CategoryFeatures,on_delete=models.CASCADE,related_name='feature_options')
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name + " " + self.feature.name        

    
class ProductModel(models.Model):

    choice=(("Normal","Normal"),("Vip","Vip"))
    currency=(
        ("Rwf","Rwf"),
        ("USD","USD")
    )
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255)
    description=models.TextField()
    shop=models.ForeignKey(ShopModel,on_delete=models.SET_NULL,null=True,blank=True)
    price=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to='product_thumbnail')
    uploader=models.ForeignKey(User,on_delete=models.CASCADE,related_name='uploader')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default='Other')
    colors=models.ManyToManyField(Colors,related_name='product_colours',null=True,blank=True)
    discount=models.IntegerField(null=True,blank=True)
    place=models.CharField(choices=choice,max_length=255,default='Normal')
    currency=models.CharField(choices=currency,max_length=100,default='Rwf')
    verified=models.BooleanField(default=False)
    rejected=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name_plural='Products'
        ordering=('-created_at',)

    def product_Image(self):
        pass  
          
class ProductImage(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='product_images')
    image=models.ImageField(upload_to='Image_pictures')
    
class ProductFeatureOptions(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='product_feature_options')
    feature=models.ForeignKey(CategoryFeatures,on_delete=models.CASCADE)
    option=models.ForeignKey(FeatureOptions,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}-{self.feature.name} - {self.option.name}" 
    class Meta:
        verbose_name = 'Product Feature Options'
        verbose_name_plural = 'Product Feature Options'
    
               
class Like(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    liker=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liker')
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE,related_name='shop_liked')
class Comment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)  
    commenter=models.ForeignKey(User,on_delete=models.CASCADE)
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.SET_NULL,null=True,blank=True)
class OurAds(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    thumbnail=models.ImageField(upload_to='OurAds/',null=False)
    name=models.CharField(max_length=255,null=False)
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{{self.name}}- {{self.id}}" 
    class Meta:
        verbose_name_plural='Our Ads'   

        