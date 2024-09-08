from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ProductImage,ProductModel,Colors,Category,Like,Comment,ShopModel,CategoryFeatures,FeatureOptions,ProductFeatureOptions,OurAds
from .serializers import ProductImageSerializer,ProductSerializer,ShopSerializer,ColorsSerializer,CategorySerializer,FeatureSerializer,ProductFeatureOptionSerializer,OurdsSerializer
from Wallet.models import MyWallet,WalletHistory
from Wallet.Serializer import MyWalletSerializer,WalletHistorySerializer
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
# Product  views here.
class ProductView(APIView):
    def get_permissions(self):
        
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]  # Require authentication for POST
        elif self.request.method == 'PUT': 
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated,]  # Require authentication for DELETE        
        else:
            self.permission_classes = [AllowAny,]  # Allow any access for other methods
        return [permission() for permission in self.permission_classes]
    def dispatch(self, request, *args, **kwargs):
        # Restrict GET requests from browsers based on User-Agent
        if request.method == 'GET' and 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        product=ProductModel.objects.all().prefetch_related('product_images')
        page_number = request.GET.get('page', 1) 
        page_size=3
        paginator = Paginator(product, page_size)  # Apply pagination
        page_obj = paginator.get_page(page_number)
        serializer=ProductSerializer(page_obj,many=True,context={"request":request})
        data = {
        'products': serializer.data,  # Serialized product data
        'has_next': page_obj.has_next(),  # Whether there's a next page
        'page': page_number,  # Current page number
    }
        return Response(data,status=200)
    
    def post(self,request):
        if not request.user.verified:
            return Response({"detail":"Not Verified"},status=401)
        serializer=ProductSerializer(data=request.data,context={'user':request.user})
        product_images = request.FILES.getlist('product_images')
        features=request.data.getlist('features')
        # print(features)
        if serializer.is_valid():
            try:
                wallet=MyWallet.objects.get(user=request.user.id)
                # print(wallet)
                if request.data['currency']=='USD':
                    price=int(request.data['price'])*1200
                else:    
                    price=int(request.data['price'])
                # print(type(price))
                if price * 0.06 > wallet.amount:
                    return Response({"detail":"You don't have enough money in your wallet"},status=401)
                else:
                   
                    
                    wallet.amount =wallet.amount-(price * 0.06)
                    wallet.save()
                    wallet_history=WalletHistory.objects.create(wallet=wallet,amount=price*0.06)
                    wallet_history.save()
                    product=serializer.save()
                    for product_image in product_images:
                        image_serializer=ProductImageSerializer(data={"product":product.id,"image":product_image})
                        if image_serializer.is_valid():
                            image_serializer.save()
                    
                        else:
                            return Response({"detail":image_serializer.errors},status=401)
                    for feature in features:
                        # print("feature",feature)
                        try:
                            feature_obj=FeatureOptions.objects.get(id=feature)
                            data={
                                "product": product.id,
                                "feature": feature_obj.feature.id,
                                "option": feature_obj.id
                            }
                            featureserializer=ProductFeatureOptionSerializer(data=data)
                            if featureserializer.is_valid():
                                featureserializer.save()
                        except FeatureOptions.DoesNotExist:
                            pass        
                    return Response({"product":serializer.data},status=201)
            except MyWallet.DoesNotExist:
                return Response({"detail":"A user has no Wallet please contact the Administrator for the wallet"},status=401)        

            
        else :
            return Response({"detail":serializer.errors},status=401)
    def put(self,request):
        serializer=ProductSerializer(data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"product":serializer.data},status=200)
        else:
            return Response({"product":serializer.errors},status=200)
    # Delete Method  
    def delete(self, request):
        try:
            product=ProductModel.objects.get(id=request.data['product_id'])
            product.delete()
            return Response({"detail":"Product deleted successfully"},status=200)   
        except ProductModel.DoesNotExist:
            return Response({"detail":"Product Does not exist"},status=401)
class filter_products(APIView):
    def get(self, request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        category_id = request.GET.get('category', None)
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        color = request.GET.get('color', None)
        feature_ids = request.GET.getlist('features', None)  # Expecting a list of feature IDs

        products = ProductModel.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

        if color:
            products = products.filter(color__iexact=color)

        if feature_ids:
            products = products.filter(features__id__in=feature_ids).distinct()

        serializer=ProductSerializer(products,many=True)
        

        return Response({'products':serializer.data},status=200)       
class VipProduct(APIView):
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        products=ProductModel.objects.filter(place='Vip')
        serializer=ProductSerializer(products,many=True,context={"request":request}) 
        return Response({"products":serializer.data},status=200) 
#Category Class
class CategoryView(APIView):
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        category=Category.objects.all()
        serializer=CategorySerializer(category,many=True,context={"request":request})
        return Response({"category":serializer.data},status=200)
    
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"category":serializer.data},status=201)
        else:
            return Response({"detail":serializer.errors},status=401)
        
class ColorViews(APIView):
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        colors=Colors.objects.all()
        serializer=ColorsSerializer(colors,many=True)
        return Response({"colors":serializer.data},status=200)
    def post(self,request):
        serializer=ColorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"color":serializer.data},status=201)
        else:
            return Response({"detail":serializer.errors},status=401)
class ShopView(APIView):
    def get_permissions(self):
        
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]  # Require authentication for POST
        elif self.request.method == 'PUT':
            self.permission_classes = [IsAuthenticated,]  # Require authentication for POST    
        else:
            self.permission_classes = [AllowAny,]  # Allow any access for other methods
        return [permission() for permission in self.permission_classes]
    def get(self,request,shop_id=None): 
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        if shop_id is None:
            shop=ShopModel.objects.all()
            serializer=ShopSerializer(shop,many=True,context={"request":request})
            return Response({"shops":serializer.data},status=200)
        else:
           try:
               shop=ShopModel.objects.get(id=shop_id)
               shop_products=ProductModel.objects.filter(shop=shop)
               product_serializer=ProductSerializer(shop_products,many=True,context={"request":request})
               serializer=ShopSerializer(shop,context={"request":request})
               return Response({"shop":serializer.data,"shop_products":product_serializer.data},status=200)
           except ShopModel.DoesNotExist:
               return Response({"detail":"Shop Does not exist"},status=401)
    def post(self, request):
        serializer=ShopSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"shop":serializer.data},status=201)
        else:
            return Response({"detail":serializer.errors},status=401)
    def put(self,request,shop_id):
        try:
            shop=ShopModel.objects.get(id=shop_id)
        except ShopModel.DoesNot:
            return Response({"detail":"Shop Does not exist"},status=401)    
        serializer=ShopSerializer(shop,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"shop":serializer.data},status=200)
        else:
            return Response({"detail":serializer.errors},status=401)
    def delete(self,request,shop_id):
        try:
            shops=ShopModel.objects.get(id=shop_id)
        except ShopModel.DoesNotExist:
            return Response({"detail":"Shop Does not exist"},status=401)    
        
        shops.delete()
        return Response({"detail":"Shops Deleted Successfully"},status=200)    

# Special Functions for Shops

class UserShops(APIView):
    permission_classes=[IsAuthenticated]           
    def get(self, request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        shops=ShopModel.objects.filter(owner=request.user.id)
        serializer=ShopSerializer(shops,many=True,context={"request":request})
        return Response({"shops":serializer.data},status=200)
    # def post(self,request):
    #     serializer=ShopSerializer(data=request.data,context={'user':request.user})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"shop":serializer.data},status=201)
    #     else:
    #         return Response({"detail":serializer.errors},status=401)
    # def delete(self, request):
    #     shops=ShopModel.objects.filter(owner=request.user.id)
    #     shops.delete()
    #     return Response({"detail":"Shops Deleted Successfully"},status=200)
    # def put(self,request):
    #     serializer=ShopSerializer(data=request.data,partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"shop":serializer.data},status=200)
    #     else:
    #         return Response({"detail":serializer.errors},status=401)

class FeatureView(APIView):
    def get(self,request,category_id=None):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        if category_id:
            try:
                category=Category.objects.get(id=category_id)
                features=CategoryFeatures.objects.filter(category=category)
                serializer=FeatureSerializer(features,many=True)
                return Response({"features":serializer.data},status=200)
            except Category.DoesNotExist:
                return Response({"detail":"Category Does not exist"},status=401)
        else:
            features=CategoryFeatures.objects.all()
            serializer=FeatureSerializer(features,many=True)
            return Response({"features":serializer.data},status=200)    
    def post(self,request):
        serializer=FeatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
class OurAdsView(APIView):
    def get(self, request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        ads=OurAds.objects.all()
        serializer=OurdsSerializer(ads,many=True)
        return Response({"oursAds":serializer.data},status=200)
         
