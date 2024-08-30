from django.contrib import admin
from .models import ProductModel,ProductImage,Colors,Category,Like,Comment,ShopModel,ShopCategory,OurAds,ProductFeatureOptions,FeatureOptions,CategoryFeatures
# Register your models here.
admin.site.register(ProductModel)
admin.site.register(ProductImage)
admin.site.register(Colors)
# admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ShopModel)
admin.site.register(OurAds)
admin.site.register(ShopCategory)
class FeatureOptionsInline(admin.TabularInline):
    model = FeatureOptions
    extra = 1
class CategoryFeaturesAdmin(admin.ModelAdmin):
    inlines = [FeatureOptionsInline]

class CategoryFeaturesInline(admin.TabularInline):
    model = CategoryFeatures
    extra = 1
    inlines = [FeatureOptionsInline]
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryFeaturesInline]

admin.site.register(Category, CategoryAdmin)        
admin.site.register(ProductFeatureOptions)
admin.site.register(FeatureOptions)
admin.site.register(CategoryFeatures, CategoryFeaturesAdmin)
# admin.site.register(CategoryFeatures)

