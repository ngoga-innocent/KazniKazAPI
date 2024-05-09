from django.contrib import admin
from .models import ProductModel,ProductImage,Colors,Category,Like,Comment
# Register your models here.
admin.site.register(ProductModel)
admin.site.register(ProductImage)
admin.site.register(Colors)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)

