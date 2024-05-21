from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ProductImage,ProductModel,Colors,Category,Like,Comment
from .serializers import ProductImageSerializer,ProductSerializer,ColorsSerializer,CategorySerializer
from Wallet.models import MyWallet,WalletHistory
from Wallet.Serializer import MyWalletSerializer,WalletHistorySerializer
# Product  views here.
class ProductView(APIView):
    def get_permissions(self):
        
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]  # Require authentication for POST
        else:
            self.permission_classes = [AllowAny,]  # Allow any access for other methods
        return [permission() for permission in self.permission_classes]
    def get(self,request):
        product=ProductModel.objects.all().prefetch_related('product_images')
        serializer=ProductSerializer(product,many=True,context={"request":request})
        return Response({"products":serializer.data},status=200)
    
    def post(self,request):
        serializer=ProductSerializer(data=request.data,context={'user':request.user})
        product_images = request.FILES.getlist('product_images')
        if serializer.is_valid():
            try:
                wallet=MyWallet.objects.get(user=request.user.id)
                print(wallet)
                price=int(request.data['price'])
                print(type(price))
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
        

#Category Class
class CategoryView(APIView):
    def get(self,request):
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