from rest_framework import serializers
from .models import ProductImage,ProductModel,ShopModel,Category,Colors
from Account.serializers import UserSerializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Colors
        fields='__all__'
class ProductSerializer(serializers.ModelSerializer):
    uploaded_images=ProductImageSerializer(read_only=True,many=True,source='product_images')
    
    category_details=CategorySerializer(source='category',read_only=True)
    colors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Colors.objects.all(),
        required=False  # Optional, depending on whether you require colors to be specified
    )
    uploader=UserSerializer(read_only=True)
    class Meta:
        model=ProductModel
        fields=['id','name','price','thumbnail','colors','category','category_details','discount','place','description','uploader','uploaded_images']
    def create(self, validated_data):
        validated_data['uploader']=self.context['user']
        colors = validated_data.pop('colors', [])
        product= ProductModel.objects.create(**validated_data)
        product.colors.set(colors)
        return product
