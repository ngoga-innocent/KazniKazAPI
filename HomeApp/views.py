from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render,redirect
from django.views import View
from Product.models import Category,ProductModel,OurAds,ProductImage,ProductFeatureOptions,ShopModel,ShopCategory,CategoryFeatures,FeatureOptions
from Wallet.models import MyWallet,WalletHistory
from Product.serializers import CategorySerializer,FeatureSerializer
from django.db.models import Q
from Account.firebase import send_push_notification
import os
import json
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.db.models import Count
from .home_forms import ProductForm,ShopForm
from django.core.paginator import Paginator
# Create your views here.

class LoginView(View):
    def get(self, request,*args,**kwargs):
        action=kwargs.get('action')
        if action=='login':
            return render(request, 'Login/Login.html')
    def post(self, request, *args,**kwargs):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            next_url = request.GET.get('next', 'homepage')
            return redirect(next_url)
        else:
            return render(request, 'Login/Login.html',{'error':'Invalid Credentials'})   
class RegisterView(View):
    def get(self, request,*args,**kwargs):
        action=kwargs.get('action')
        if action =='register':
            form=UserRegistrationForm()
            return render(request, 'Login/Register.html',{"form":form}) 
    def post(self,request,*args,**kwargs):
        form=UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            # send_push_notification(user.fcm_token, f"Welcome to KazniKaz {user.username}!", 'default')
            return redirect('login')
        else:
            return render(request, 'Login/Register.html',{'errors': form.errors,"form":form})            
class HomeView(View):
    def get(self, request,pk=None):
        if pk is not None:
            product=ProductModel.objects.get(pk=pk)
            context={'product': product}
            return render(request, 'ProductPage.html',context)
        
        
        categories = Category.objects.filter(parent=None).order_by('name')
        categories_with_products = Category.objects.annotate(product_count=Count('productmodel')).order_by('-product_count', 'name')[:4]
        admin_product=ProductModel.objects.filter(place='Vip')
        
        new_product=ProductModel.objects.filter(Q(place='Vip') | Q(discount__gte=0)).order_by('-created_at')[:12]
        discount_products=ProductModel.objects.filter(discount__gte= 0)
        print(discount_products)
        our_ads=OurAds.objects.all()
        context={'categories': categories,'new_products': new_product,'discounts':discount_products,'our_ads': our_ads,"category_products":categories_with_products,"admin_products":admin_product}
        return render(request, 'Homepage.html',context)
class ProductView(View):
    def get(self, request,id=None,*args,**kwargs):
        action=kwargs.get('action')
        if id is not None:
            try:
                product=ProductModel.objects.get(id=id)
                product_images=ProductImage.objects.filter(product=product)
                product_feature=ProductFeatureOptions.objects.filter(product=product)
                related_products=ProductModel.objects.filter(Q(uploader=product.uploader)|Q(shop=product.shop)|Q(category=product.category))
                context={'product': product,"product_images": product_images,"product_features": product_feature,"related_products": related_products}
                return render(request, 'Products/singleproduct.html',context)
            except ProductModel.DoesNotExist:
                context={}
                return render(request, 'Products/products.html',context)
        if action=='upload_product':
            if not request.user.is_authenticated:
                return redirect('login')
            parent_category=Category.objects.filter(parent=None)
            user_shops=ShopModel.objects.filter(owner=request.user)
            form=ProductForm()
            return render(request, 'Products/add_product.html', {"form": form,"categories": parent_category,"shops":user_shops})    
        products=ProductModel.objects.all().order_by('-created_at')
        context={'products': products}
        return render(request, 'Products/products.html',context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.uploader = request.user
            wallet =MyWallet.objects.get(user=request.user)
            print(wallet.amount)
            string_price=request.POST.get('price')
            price=float(string_price)
            if wallet.amount < price*0.06:
                return JsonResponse({"error": "Insufficient funds to Add This product"}, status=400)
            wallet.amount =wallet.amount - (price * 0.06)
            WalletHistory.objects.create(amount=wallet.amount,wallet=wallet,action=f'Upload Product '+str(product.name),status='Success')
            wallet.save()
            product.save()

            # Handle multiple images
            for image in request.FILES.getlist('uploaded_files'):
                ProductImage.objects.create(product=product, image=image)
            
            # Handle product features
            features_json = request.POST.get("product_features")
            print(features_json)
            if features_json:  # Check if features_json is provided
                try:
                    features = json.loads(features_json)
                    for feature in features:
                        product_option = feature.get('option')
                        product_feature = feature.get('feature')
                        try:
                            feature=CategoryFeatures.objects.get(id=product_feature)
                            option=FeatureOptions.objects.get(id=product_option)
                        except FeatureOptions.DoesNotExist or CategoryFeatures.DoesNotExist:
                            return JsonResponse({"error": "Feature or option not found"}, status=400)
                        # Validate that both feature and option are provided
                        if product_feature and product_option:
                            product_fature=ProductFeatureOptions.objects.create(
                                product=product,
                                feature=feature,
                                option=option
                            )
                            print(product_fature)
                        else:
                            return JsonResponse(
                                {"error": "Feature or option missing in the provided data"},
                                status=400
                            )
                    
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid feature data"}, status=400)

            # If everything is processed successfully
            return JsonResponse({"success": True}, status=201)
        
        else:
            # Return form errors if form is not valid
            return JsonResponse({"error": form.errors}, status=400)
            # return render(request, 'Products/add_product.html',{'errors': form.errors,"form":form})    
class CategoryView(View):
    def get(self, request,id=None):
        if id is not None:
            try:
                category=Category.objects.get(id=id)
                related_categories=Category.objects.filter(Q(parent=category))
                products=category.productmodel_set.all()
                paginator=Paginator(products,25)
                page_number=request.GET.get('page')
                page_obj=paginator.get_page(page_number)
                context={'category': category,'products': page_obj,'related_categories': related_categories}
                return render(request, 'Products/products.html',context)
            except Category.DoesNotExist:
                context={}
                return render(request, 'Products/products.html',context)    
class AboutUsView(View):
    def get(self, request):
        return render(request, 'AboutUs.html') 
class ShopView(View):
    
    def get(self, request, id=None,*args, **kwargs):
        action=kwargs.get('action')
        if action=='search':
            query=request.GET.get('search_text','').strip()
            if query:
                shops=ShopModel.objects.filter(Q(name__icontains=query) | Q(location__icontains=query)|Q(slug__contains=query))
            else:
                shops=ShopModel.objects.all()    
            
            paginator=Paginator(shops,15)
            page_number=request.GET.get('page')
            page_obj=paginator.get_page(page_number)
            context={'shops': page_obj}
            
            html=render(request, 'Shop/partial.html',context).content.decode('utf-8')
            return JsonResponse({"html":html})
        elif action=='new_shop':
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.verified:
                form=ShopForm()
                return render(request, 'Shop/add_shop.html', {"form": form})
            else:
                return redirect('verify')
        if id is not None:
            if  action=='shop_category':
                try:
                    shop_category=ShopCategory.objects.get(id=id)
                    shops=ShopModel.objects.filter(shop_category=shop_category)
                    paginator=Paginator(shops,15)
                    page_number=request.GET.get('page')
                    page_obj=paginator.get_page(page_number)
                    context={'shops': page_obj} 
                    html=render(request, 'Shop/partial.html',context).content.decode('utf-8')
                    return JsonResponse({"html":html})
                except ShopCategory.DoesNotExist:
                    shops=ShopModel.objects.all()
                    paginator=Paginator(shops,15)
                    page_number=request.GET.get('page')
                    page_obj=paginator.get_page(page_number)
                    shop_category=ShopCategory.objects.all()
                    print("shopdetails")
                    context={'shops': page_obj,'shop_categories':shop_category}
                    
                    return render(request, 'Shop/shops.html',context)  
            elif  action=='shop_details':
                try:
                    shop=ShopModel.objects.get(id=id)
                    products=ProductModel.objects.filter(shop=shop)
                    paginator=Paginator(products,2)
                    page_number=request.GET.get('page')
                    page_obj=paginator.get_page(page_number)
                    context={'shop': shop,'products': page_obj}
                    return render(request, 'Shop/shop_details.html',context)
                except ShopModel.DoesNotExist:
                    context={}
                    return render(request, 'Shop/shops.html',context)
                      
        shops=ShopModel.objects.all()
        paginator=Paginator(shops,15)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        shop_category=ShopCategory.objects.all()
       
        context={'shops': page_obj,'shop_categories':shop_category} 
        return render(request, 'Shop/shops.html',context)  
    def post(self, request):
        form=ShopForm(request.POST,request.FILES)
        if request.user.verified:
            if form.is_valid():
                shop=form.save(commit=False)
                shop.owner=request.user
                shop.save()
                return redirect('web_shops')
            else:
                return render(request,'shop/add_shop.html',{'form':form,"errors":form.errors})
# Uplaod Product
def categorychildren(request):
    parent_id=request.GET.get('parent_id')
    try:
        category=Category.objects.get(id=parent_id)
        features=CategoryFeatures.objects.filter(category=category)
        features_serialize=FeatureSerializer(features,many=True)
        children=Category.objects.filter(parent=category)
        serializer=CategorySerializer(children,many=True)
        return JsonResponse({"children":serializer.data,"features":features_serialize.data})
    except Category.DoesNotExist:
        return JsonResponse({"error":"Invalid Category"})    
def serve_assetlinks_json(request):
    assetlinks_json_path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(assetlinks_json_path, 'r') as file:
        return HttpResponse(file.read(), content_type='application/json')   
def Privacy(request):
    return render(request, 'Privacy.html')     
