from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from Product.models import Category,ProductModel,OurAds,ProductImage,ProductFeatureOptions,ShopModel,ShopCategory,CategoryFeatures,FeatureOptions
from Wallet.models import MyWallet,WalletHistory
from Product.serializers import CategorySerializer,FeatureSerializer
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Account.firebase import send_push_notification
import os
import json
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from .forms import UserRegistrationForm,PostJob
from django.db.models import Count
from .home_forms import ProductForm,ShopForm
from django.core.paginator import Paginator
from Account.models import User
from django.utils import timezone
from collections import defaultdict
from datetime import timedelta
from rest_framework.response import Response
from Jobs.models import Job,JobCategoryChoice
from Chat.models import Room,Message
from Account.models import Notifications
from Account.serializers import NotificationSerializer,UserSerializer
from News.models import New
from django.db.models import OuterRef, Subquery
from Wallet.models import MyWallet,WalletHistory,Payments
# from rest_framework.response import Response
from django.http import JsonResponse
from Wallet.Serializer import WalletHistorySerializer,MyWalletSerializer
from Wallet.SendEmail import sending_email

import requests
import json
import time
from django.views.decorators.csrf import csrf_exempt
client_id="4645d206-48c1-11ef-a6a2-deade826d28d", 
client_secret="76ff484a244047ecbbc3ffeca5dc79a3da39a3ee5e6b4b0d3255bfef95601890afd80709"
# client_id="66d24278-48cd-11ef-82f6-deade826d28d"
# client_secret="238196c663cfa65f6c0220db4426733cda39a3ee5e6b4b0d3255bfef95601890afd80709"
Base_url="https://payments.paypack.rw/api"
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
class ForgotPassword(View):
    def get(self,request):
        return render(request,'Login/forgot_password.html')       
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')        
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
class requestVerification(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Login/Verification.html')
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user=request.user
            phone_Number=request.POST.get('phone_number')
            id_number=request.POST.get('id_no')
            email=request.POST.get('email')
            id_card=request.FILES.get('id_card')
            selfie=request.FILES.get('selfie')
            if phone_Number:
                user.phone_number=phone_Number
            if id_number:
                user.id_number=id_number
            if email:
                user.email=email    
            if id_card:
                user.id_card=id_card
            if selfie:
                user.selfie=selfie
            user.account_status="Pending"    
            user.save()    
            
            return redirect('homepage')
            
            # print(request.POST)
            # print(request.FILES)
            # data = {**request.POST, **request.FILES}
            # serializer = UserSerializer(user, data=data, partial=True, context={"request": request})
            # if serializer.is_valid():
            #     user=serializer.save()
            #     user.account_status="Pending"
            #     user.save()
            #     return JsonResponse({"detail":"Verification details sent to Kaz ni Kaz Staff you will be reached out in 2-5 working days"})
            # else:
            #     print(serializer.errors)
            #     return JsonResponse({"detail":serializer.errors},status=400)
        else:
            return redirect('login')                       
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
        wallet=False
        if request.user.is_authenticated:
            try:
                wallet=MyWallet.objects.get(user=request.user)
            except MyWallet.DoesNotExist:
                wallet=False    
        our_ads=OurAds.objects.all()
        context={'wallet':wallet,'categories': categories,'new_products': new_product,'discounts':discount_products,'our_ads': our_ads,"category_products":categories_with_products,"admin_products":admin_product}
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
            if not request.user.verified:
                return redirect('verify')
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
            currency=request.POST.get('currency')
            
            price=float(string_price)
            if currency == 'USD':
                price=price * 1200
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
def FilterProduct(request):
    option_id=request.GET.get('option_id')
    print(option_id)
    try:
         option=FeatureOptions.objects.get(id=option_id)
         products_with_choosen_option=ProductFeatureOptions.objects.filter(option=option)
         products=[product.product for product in products_with_choosen_option]
         return render(request,'Products/partial.html',{"products": products})
    except FeatureOptions.DoesNotExist:
        category_id=request.GET.get('category_id')
        try:
            category=Category.objects.get(id=category_id)
            products=ProductModel.objects.filter(category=category).order_by('-created_at')
            return render(request,'Products/partial.html',{"products": products})
        except Category.DoesNotExist:
            products=ProductModel.objects.all().order_by('-created_at')[:50]
            context={"products": products}
            return render(request, 'Products/partial.html',context)
def filterProductByMinandMax(request):
    min_price=request.GET.get('min')
    max_price=request.GET.get('max')
    category_id=request.GET.get('category_id')
    currency=request.GET.get("currency")
        
    try:
        min_price=int(min_price)
        max_price=int(max_price)
        
        try:
            category=Category.objects.get(id=category_id)
            if max_price == 0:
                products=ProductModel.objects.filter(category=category).order_by('-created_at')[:50]
            else:    
                products=ProductModel.objects.filter(Q(price__gte=min_price,price__lte=max_price,currency=currency),category=category).order_by('-created_at')
        except Category.DoesNotExist:
                products=ProductModel.objects.all().order_by('-created_at')[:50]    
           
            
        return render(request,'Products/partial.html',{"products": products})
    except ValueError:
        products=ProductModel.objects.all().order_by('-created_at')[:50]
        context={"products": products}
        return render(request, 'Products/partial.html',context)
def SearchProduct(request):
    keyword=request.GET.get('query','')
    products=ProductModel.objects.filter(name__icontains=keyword).order_by('-created_at')
    return render(request,'Products/partial.html',{"products": products})
                          
class CategoryView(View):
    def get(self, request,id=None):
        if id is not None:
            try:
                category=Category.objects.get(id=id)
                related_categories=Category.objects.filter(Q(parent=category)|Q(parent=category.parent)).exclude(id=category.id)
                category_features=category.getCategoryFeatures()
                products=category.productmodel_set.all()
                paginator=Paginator(products,25)
                page_number=request.GET.get('page')
                page_obj=paginator.get_page(page_number)
                context={'category': category,'products': page_obj,'related_categories': related_categories,"features":category_features}
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
    
class ChatView(View):
    def get(self, request,uploader_id=None):
        if request.user.is_authenticated:
            if uploader_id is not None:
                print(request.user.id)
                print(uploader_id)
                try:
                    uploader=User.objects.get(id=uploader_id)
                    if uploader != request.user:
                        room1_exist=Room.objects.filter(user1=uploader,user2=request.user).exists()
                        room2_exist=Room.objects.filter(user1=request.user, user2=uploader).exists()
                        if room1_exist:
                            room=Room.objects.get(user1=uploader, user2=request.user)
                        elif room2_exist:
                            room=Room.objects.get(user2=uploader, user1=request.user) 
                        else:
                            room=Room.objects.create(user2=uploader, user1=request.user)       
                        # room, created = Room.objects.get_or_create(Q(user1=request.user, user2=uploader)|Q(user1=uploader, user2=request.user))
                        # messages=room.message_set.all().order_by('timestamp')
                        # all_rooms=Room.objects.filter(Q(user1=request.user)|Q(user2=request.user)).order_by('-timestamp')
                        # print(room)
                        return JsonResponse({"success": True,"room":room.id},status=200)
                    else:
                        return redirect('web_products')
                except User.DoesNotExist:
                    return redirect('web_products')
            else:
                    
                user=request.user
                chats=Room.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-timestamp')
                return render(request, 'Chat/All_chat.html', {'all_rooms': chats})
        else:
            return redirect('login')
    def post(self, request):
        room_id = request.POST.get('room_id')
        print(room_id)
        message_text = request.POST.get('message')

        room = get_object_or_404(Room, id=room_id)
        if room.user1==request.user:
            receiver=room.user2
        else:
            receiver=room.user1    
        new_message = Message.objects.create(
            room=room,
            sender=request.user,
            receiver=receiver,
            message=message_text,
            timestamp=timezone.now()
        )
        room.last_message=new_message.message
        room.save()

        # Return the new message rendered as HTML
        return render(request, 'Chat/partials/message.html', {'message': new_message})
    
@login_required
def load_messages(request):
    """View to load messages via AJAX."""
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by('-timestamp')

    # Prepare dates for comparison
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    grouped_messages = defaultdict(list)
    for message in messages:
        date_key = timezone.localtime(message.timestamp).date()
        grouped_messages[date_key].append(message)
    grouped_messages=dict(grouped_messages)
    return render(request, 'Chat/partials/messages.html', {
        'grouped_messages': grouped_messages,
        'today': today,
        'yesterday': yesterday
    })
@login_required
def load_room(request):
    user = request.user

    # Subquery to get the latest message's timestamp in each room
    latest_message_subquery = Message.objects.filter(room=OuterRef('pk')).order_by('-timestamp').values('timestamp')[:1]

    # Get all rooms the user is a part of, and annotate with the latest message timestamp
    all_rooms = Room.objects.filter(Q(user1=user) | Q(user2=user)) \
                .annotate(latest_message=Subquery(latest_message_subquery)) \
                .order_by('-latest_message')

    return render(request, 'Chat/partials/all_rooms.html', {'all_rooms': all_rooms})
       

# JOb View
class JobView(View):
    def get(self, request,id=None, *args, **kwargs):
        if id is not None:
            try:
                job=Job.objects.get(id=id)
                context={'job': job}
                return render(request, 'Job/job_details.html',context)
            except Job.DoesNotExist:
                return redirect('jobs')
        jobs=Job.objects.all()
        ourads=OurAds.objects.all().order_by('-created_at')[:10]
        categories=JobCategoryChoice.objects.all()
        paginator=Paginator(jobs,15)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={'jobs': page_obj,"categories":categories,"our_ads":ourads}
        return render(request, 'Job/jobs.html',context)
    def post(self,request):
        form=PostJob(request.POST,request.FILES)
        if form.is_valid():
            job=form.save(commit=False)
            job.job_provider=request.user
            job.save()
            return redirect('homepage')
        else:
            print(form.errors)
            return render(request, 'Job/postjob.html',{"form":form,"errors":form.errors})
def JobFilter(request):
    category_id=request.GET.get('category')
    try:
        category=JobCategoryChoice.objects.get(id=category_id)
        jobs=Job.objects.filter(job_category=category).order_by('-created_at')
        print(category)
    except JobCategoryChoice.DoesNotExist:
            jobs=Job.objects.all().order_by('-created_at')
    
    paginator=Paginator(jobs,15)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    print(jobs)
    context={'jobs': page_obj}
    return render(request, 'Job/job_partial.html',context)
def JobSearch(request):
    job_query=request.GET.get("search_job",'')
    if job_query is not None:
        jobs=Job.objects.filter(Q(job_title__icontains=job_query) | Q(job_description__icontains=job_query))
    else:
        jobs=Job.objects.all().order_by('-created_at')    
    paginator=Paginator(jobs,15)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    print(jobs)
    context={'jobs': page_obj}
    return render(request, 'Job/job_partial.html',context)
def JobPost(request):
    if request.user.is_authenticated:
        form=PostJob()
        return render(request, 'Job/postjob.html',{"form":form})
    else:
        return redirect('login')
    
class NewsView(View):
    def get(self, request):
        news=New.objects.all().order_by('-created_at')
        today=timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        today_news=New.objects.filter(created_at__date=today).order_by('-created_at')
        if len(today_news) == 0:
            today_news = New.objects.all().order_by('-created_at')[:5]
        week_news = New.objects.filter(created_at__date__gte=start_of_week).order_by('-created_at')
        if len(week_news) == 0:
            week_news = New.objects.excludee(pk__in=today_news).order_by('-created_at')[:5]  # If no news for the week, show all news for the day.
        remaining_news = New.objects.exclude(pk__in=today_news).exclude(pk__in=week_news).order_by('-created_at')
        paginator=Paginator(remaining_news,50)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={'news': page_obj,"today_news":today_news,"week_news":week_news}
        return render(request, 'News/news.html',context) 
class WalletWeb(View):
    # permission_classes=[IsAuthenticated]
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        user=request.user
        
        try:
            wallet=MyWallet.objects.get(user=user)
            history=WalletHistory.objects.filter(wallet=wallet).order_by('-created_at')
            serializer=MyWalletSerializer(wallet)
            historySerializer=WalletHistorySerializer(history,many=True)
            context={"wallet":wallet,"histories":history}
            return render(request,"Wallet/wallet.html",context)
        except MyWallet.DoesNotExist:
            return render(request,"Wallet/wallet.html")
    # def post(self,request):
    #     user=request.user
    #     try:
    #         MyWallet.objects.get(user=user)
    #         return Response({'detail':f'wallet for this user exists'},status=400)
    #     except MyWallet.DoesNotExist:
    #         data={'user':user.id}
    #         seriazer=MyWalletSerializer(data=data,context={"request":user})
            
    #         if seriazer.is_valid():
    #             seriazer.validated_data['user']=user
    #             seriazer.save()
    #             return Response({"wallet":"Wallet created successfully"},status=200)
    #         else:
    #             return Response({"details":seriazer.errors},status=401)
    
                
    def post(self,request):
        action=request.POST.get('action')
        amount=request.POST.get('amount')
       
        try:
           
            
            wallet=MyWallet.objects.get(user=request.user)
            if action=='Deposit':
                print("deposit")
                phone_number=request.POST.get('phone_number')
                amount=float(amount)
                cashin=self.Deposit(amount,phone_number,"Deposit")
                # print(cashin.json().get('ref'))
                if cashin.status_code==200:
                    
                    amount=amount-(amount*0.02)
                    # print("status _code verified")
                    history=WalletHistory.objects.create(
                        wallet=wallet,
                        action=action,
                        amount=amount,
                        payment_ref=cashin.json().get('ref')
                    )
                    
                    return JsonResponse({"detail":f"Check the prompt sent to "+ phone_number +" or dial *182*7*1# to complete Payment process"},status=200)
                    
                else:
                     return JsonResponse({"detail":"Payment Failed"},status=400)
            # if amount > wallet.amount and action !='Deposit':
            #         return JsonResponse({"detail":"insuficient Amount"},status=400)
            # if action=='Withdraw':
            #     phone_number=request.data['phone_number']
            #     cashout=self.Withdraw(amount,phone_number,"Withdraw")
            #     if cashout.status_code==200:

            #         ref=cashout.json().get('ref')
            #         history=WalletHistory.objects.create(
            #             wallet=wallet,
            #             action='Withdraw',
            #             amount=amount,
            #             payment_ref=ref
            #         )
            #         # wallet.save()
            #         # sending_email(request.user,'Withdraw made Successfully',f'Dear ' + request.user.username + ' Your Withdraw of ' + str(amount) +' Rwf has been made successfully ')
            #         walletSerializer=MyWalletSerializer(wallet)
            #         HistorySerializer=WalletHistorySerializer(history)
            #         return Response({"data":{
            #             "wallet":walletSerializer.data,
            #             "history":HistorySerializer.data
            #         }})
            elif action =='Transfer':
                reciever=request.POST.get('wallet')
                if float(amount) < 1000:
                    return JsonResponse({"detail":"Transfer amount should not be less Than 1000 Rwf","success":False},status=200)
                try:
                    
                    reciever_object=MyWallet.objects.get(id=reciever)
                    if reciever_object.user == request.user:
                        return JsonResponse({"detail":"Can't transfer to your own wallet","success":False},status=200)
                    amount=float(amount)
                    wallet.amount=wallet.amount-amount
                    reciever_object.amount =reciever_object.amount + amount
                    history=WalletHistory.objects.create(
                        wallet=wallet,
                        action='Transfer',
                        amount=amount,
                        reciever=reciever_object
                    )
                    wallet.save()
                    reciever_object.save()
                    sending_email(request.user,'Transfer made Successfully',f'Dear ' + request.user.username + ' Your Transfer of ' + str(amount) +' Rwf has been made successfully ')
                    sending_email(reciever_object.user,'Transfer made Successfully',f'Dear ' + reciever_object.user.username + ' Your Transfer of ' + str(amount) +' Rwf has been made successfully transfered to your account ')
                    
                    return JsonResponse({"detail":"Transfer made Successfully","success":True},status=200)
                except MyWallet.DoesNotExist:
                    return JsonResponse({'details':'invalid reciever wallet address',"success":False},status=400)
        except MyWallet.DoesNotExist:
            return JsonResponse({"detail":"Wallet Doesn't exist"},status=404)
    def authorization(self):
        url = "https://payments.paypack.rw/api/auth/agents/authorize"
        payload = json.dumps({
        "client_id": "4645d206-48c1-11ef-a6a2-deade826d28d",
        "client_secret":client_secret
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)  
        # print(response.json())
        return response.json()

    def Deposit(self,amount,phone_number,action):
          url=f'{Base_url}/transactions/cashin'
          payload = json.dumps({
            "amount": amount,
            "number": phone_number
            })
        #   print(self.authorization()['access'])
          headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.authorization()["access"]}',
            'X-Webhook-Mode':'production'
            }
          response = requests.request("POST", url, headers=headers, data=payload)
          print(response.json())
          if response.status_code==200:
              ref=response.json().get('ref')
              status=response.json().get('status')
              amount=response.json().get('amount')
              user=self.request.user
              Payments.objects.create(referenceKey=ref, amount=amount, payer=user,status=status,number=phone_number,action=action)
          ref=response.json().get('ref')
          
                
          return response
    def Withdraw(self,amount,phone_number,action):
        url = f"{Base_url}/transactions/cashout"

        payload = json.dumps({
        "amount": amount,
        "number": phone_number
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.authorization()["access"]}',
        'X-Webhook-Mode':'production',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.json())
        if not response.status_code:
            return response.json()
        elif response.status_code==200:
              ref=response.json().get('ref')
              status=response.json().get('status')
              amount=response.json().get('amount')
              user=self.request.user
              Payments.objects.create(referenceKey=ref, amount=amount, payer=user,status=status,number=phone_number,action=action)
              return response
        

    def CheckTransaction(self,referenceKey):
        url=f'{Base_url}/events/transactions?ref={referenceKey}'
        
        payload={}
        headers = {'Authorization': f'Bearer {self.authorization()["access"]}'}

        response = requests.request("GET", url, headers=headers, data=payload)
        transaction_status=response.json()
        print(transaction_status)
        status=transaction_status['transactions'][0].get('data')['status']
        print(status)
        if transaction_status['total']>1:
            try:
                payment=Payments.objects.get(referenceKey=referenceKey)
                payment.status=status
            except Payments.DoesNotExist:
                return False


        return status    
#     def cashin(self):
#         HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
#         cashin = Transaction().cashin(amount=100, phone_number="0782214360")
        
#         print(cashin)
      
#         return Response({"text":"okay"})
#     def cashout(self):
#         HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
#         cashout = Transaction().cashout( amount=100,phone_number="0782214360")
#         print(cashout)
#         return cashout
# def events(request):
#         HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
#         kind='cashout'  
#         limit=10
#         offset=0
#         all_events = Event().list(limit)

#         print(all_events)
#         return JsonResponse({"events": all_events})
# def AdminAccount(request):
#     HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
#     account=Merchant().me()
#     # print(Merchant().me())
#     return JsonResponse({"account": account})      
class Notification(View):
    def get(self, request, *args, **kwargs):
        action=kwargs.get("action")
        two_days_ago = timezone.now() - timedelta(days=2)
        if action =="count_not":
            if request.user.is_authenticated:
                count=Notifications.objects.filter(Q(User=request.user, is_read=False) | Q(type="App",timestamp__gte=two_days_ago)).count()
                return JsonResponse({"count": count})
            
            count=Notifications.objects.filter(type="App",timestamp__gte=two_days_ago).count()
            return JsonResponse({"count": count})
        else:
            if request.user.is_authenticated:
                notifications=Notifications.objects.filter(Q(User=request.user, is_read=False) | Q(type="App",timestamp__gte=two_days_ago) )
            else:
                notifications=Notifications.objects.filter(type="App",timestamp__gte=two_days_ago)    
                seerializer=NotificationSerializer(notifications,many=True)
            return render(request,"notification_base.html",{"notifications": notifications})
def serve_assetlinks_json(request):
    assetlinks_json_path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(assetlinks_json_path, 'r') as file:
        return HttpResponse(file.read(), content_type='application/json')   
def Privacy(request):
    return render(request, 'Privacy.html')     
