from rest_framework import serializers
from .models import ProductImage,ProductModel,ShopModel,Category,Colors,CategoryFeatures,FeatureOptions,ProductFeatureOptions,OurAds
from Account.serializers import UserSerializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__'
class FeatureOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FeatureOptions
        fields='__all__'        
class FeatureSerializer(serializers.ModelSerializer):
    feature_options=FeatureOptionsSerializer(read_only=True,many=True)
    class Meta:
        model=CategoryFeatures
        fields=['id', 'name', 'category','feature_options']
              
class CategorySerializer(serializers.ModelSerializer):
    category_features=FeatureSerializer(read_only=True,many=True)
    class Meta:
        model=Category
        fields=['id','name','thumbnail','parent','category_features']
class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Colors
        fields='__all__'
class ShopSerializer(serializers.ModelSerializer):
    owner=UserSerializer(read_only=True)
    class Meta:
        model=ShopModel
        fields='__all__'
    def create(self, validated_data):
        validated_data['owner'] =self.context['user']
        return ShopModel.objects.create(**validated_data) 
class ProductFeatureOptionSerializer(serializers.ModelSerializer):
    option_details=FeatureOptionsSerializer(read_only=True,source='option')
    feature_options=FeatureSerializer(read_only=True,source='feature')
    class Meta:
        model=ProductFeatureOptions
        fields=['id','product','feature','option','option_details','feature_options']     
class ProductSerializer(serializers.ModelSerializer):
    uploaded_images=ProductImageSerializer(read_only=True,many=True,source='product_images')
    features=ProductFeatureOptionSerializer(read_only=True,many=True,source='product_feature_options')
    category_details=CategorySerializer(source='category',read_only=True)
    colors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Colors.objects.all(),
        required=False  # Optional, depending on whether you require colors to be specified
    )
    colors_details=ColorsSerializer(source='colors',many=True,read_only=True)
    shop_details=ShopSerializer(source='shop',read_only=True)
    uploader=UserSerializer(read_only=True)
    class Meta:
        model=ProductModel
        fields=['id','name','price','currency','thumbnail','colors','shop','shop_details','colors_details','category','category_details','discount','place','description','uploader','uploaded_images','features']
    def create(self, validated_data):
        validated_data['uploader']=self.context['user']
        colors = validated_data.pop('colors', [])
        
        product= ProductModel.objects.create(**validated_data)
        product.colors.set(colors)
        
        return product
class OurdsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OurAds
        fields='__all__'    
