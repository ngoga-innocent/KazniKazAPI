from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from Product.models import ProductModel,Category,ProductImage,CategoryFeatures,FeatureOptions,ShopModel
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.functions import TruncMonth
from Product.serializers import CategorySerializer,ProductSerializer
from Staff.forms import CategoryForm,ProductForm,UserForm,ShopForm
from Account.models import User,Device,Notifications
from Wallet.models import MyWallet,WalletHistory
from Wallet.Serializer import MyWalletSerializer,WalletHistorySerializer
from Account.firebase  import send_push_notification
from Account.serializers import UserSerializer
from paypack.merchant import Merchant
from paypack.events import Event
from paypack.transactions import Transaction
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# Create your views here.

from paypack.client import HttpClient

client_id="4645d206-48c1-11ef-a6a2-deade826d28d", 
client_secret="76ff484a244047ecbbc3ffeca5dc79a3da39a3ee5e6b4b0d3255bfef95601890afd80709"

def is_staff(user):
    return user.is_staff

# @method_decorator([login_required, user_passes_test(is_staff)], name='dispatch')
class Home(View):
    def get(self,request):
        return render(request,'Home.html')
def product_sales_data(request):
    # Example data: You would replace this with your actual data logic
    product_counts = ProductModel.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Prepare data for the chart
    labels = [item['month'].strftime('%B %Y') for item in product_counts]
    data = [item['count'] for item in product_counts]

    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": "Number of Products",
            "backgroundColor": "rgba(75,192,192,0.4)",
            "borderColor": "rgba(75,192,192,1)",
            "borderWidth": 1,
            "data": data,
        }]
    }
    return JsonResponse(chart_data)  
class CategoryStaff(View):
    def get(self,request):
        category_id=request.GET.get('category_id')
        if category_id is not None:
            category=Category.objects.get(id=category_id)
            categories=Category.objects.filter(parent=category)
            serializer=CategorySerializer(categories,many=True)
            return JsonResponse({"children":serializer.data,"parent":CategorySerializer(category).data})
        parent_categories=Category.objects.filter(parent=None)
        context={"parent_categories":parent_categories}
        return render(request,'category/category.html',context)
    def post(self,request):
        print(request.POST,request.FILES)
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"Category Added Successfully"})
        return JsonResponse({"message":form.errors})
class AddCategoryView(View):
    def get(self,request):
        form=CategoryForm()
        context={'form':form}
        return render(request,'category/addCategory.html',context) 
    def post(self,request):
        parent_name = request.POST.get('name')
        parent_thumbnail = request.FILES.get('thumbnail')
        parent_category = Category.objects.create(
            name=parent_name, 
            thumbnail=parent_thumbnail
        )

        # Create child categories
        index = 0
        while f'child_name_{index}' in request.POST:
            child_name = request.POST.get(f'child_name_{index}')
            child_thumbnail = request.FILES.get(f'child_thumbnail_{index}')
            if child_name:
                Category.objects.create(
                    name=child_name,
                    thumbnail=child_thumbnail,
                    parent=parent_category
                )
            index += 1

        return JsonResponse({'message': 'Category and children added successfully!'})

class ProductViewStaff(View):
    def get(self,request,product_id=None,*args, **kwargs):
        action=kwargs.get('action')
        
        if action=='get_form':
            return self.get_product_form(request)
        if action=='get_edit_form':
            return self.get_product_form(request,product_id)
        categories=Category.objects.all()
        unverified_products=ProductModel.objects.filter(verified=False)
        verified_product=ProductModel.objects.filter(verified=True)
        context={'univerified_products': unverified_products,'verified_product': verified_product,'categories': categories}
        return render(request,'product/product.html',context)
    def put(self,request):
       try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
              
            if not product_id:
                return JsonResponse({'error': 'Product ID not provided'}, status=400)

            # Fetch the product based on the product_id
            product = ProductModel.objects.get(id=product_id)
            
            # Perform the approval logic
            product.verified = True  # Assuming you have an is_verified field
            product.save()

            return JsonResponse({'success': f'Product {product.name} approved successfully'})
       except ProductModel.DoesNotExist:
            print("product not found")
            return JsonResponse({'error': 'Product not found'}, status=404)
       except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    def get_product_form(self,request,product_id=None):
        if not product_id:
            form = ProductForm()
            editing=False
        else:
            product=ProductModel.objects.get(id=product_id)
            form = ProductForm(instance=product)
            editing=True 
              
        context={"form": form, "is_editing": editing, "product_id":product_id}
        return render(request,'product/add_editproduct.html',context) 
    def post(self, request,product_id=None):
        
        if product_id is not  None:
            product=ProductModel.objects.get(id=product_id)
            form=ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                product=form.save(commit=False)
                product.uploader=request.user
                product.save()
                return redirect('products')
        form=ProductForm(request.POST,request.FILES)
        uploaded_files = request.FILES.getlist('uploaded_files')
        
        if form.is_valid():
            product=form.save()
            for file in uploaded_files:
                ProductImage.objects.create(product=product, image=file)
            return redirect('products')
        return JsonResponse({"message":form.errors})
def edit_product(request,product_id):
        product=ProductModel.objects.get(id=product_id)
        form=ProductForm(instance=product)
        print("second Edit ",product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('products')
        return render(request,'product/add_editproduct.html',{'form': form}) 
def get_product_by_type(request):
    type=request.GET['type']
    print(type)
    if type=='verified':
        products=ProductModel.objects.filter(verified=True)
        serializer=ProductSerializer(products,many=True) 
        return JsonResponse(serializer.data,safe=False)
    elif type=='unverified':
        products=ProductModel.objects.filter(verified=False)
        serializer=ProductSerializer(products,many=True) 
        return JsonResponse(serializer.data,safe=False)
    elif type=='our_products':
        products=ProductModel.objects.filter(uploader=request.user)
        serializer=ProductSerializer(products,many=True) 
        return JsonResponse(serializer.data,safe=False)
    else:
        products=ProductModel.objects.all()
        serializer=ProductSerializer(products,many=True)
        return JsonResponse(serializer.data,safe=False)
class AddCategoryFeatures(View):
    def post(self, request):
        print(request.POST)
        feature=request.POST.get('feature')
        options=request.POST.getlist('options[]')
        Category_id=request.POST.get('category')
        try:
            category=Category.objects.get(id=Category_id)
        except Category.DoesNotExist:
            return JsonResponse({"message":"Category Does not exist"},status=404)  
        new_feature=CategoryFeatures.objects.create(category=category,name=feature) 
        
        if new_feature.id:
            print(new_feature.id)
            print(options)
            for option in options:
                feature_option=FeatureOptions.objects.create(feature=new_feature,name=option)  # Assuming you have an option field in FeatureOptions model.  This would create a many-to-many relationship between CategoryFeatures and FeatureOptions.  This assumes you have a many-to-many relationship between Category and CategoryFeatures.  If not, you would need to create a new model for that relationship.  
                print(option)
            return JsonResponse({"message":"Category Feature Options Added Successfully"})
            
        return JsonResponse({"message":"Category Features Added Successfully"})   
class rejectProduct(View):
    def post(self,request):
        
        product_id=request.POST.get('product_id')
        message=request.POST.get('message')
        
        try:
            product=ProductModel.objects.get(id=product_id)
            try:
                uploader_device=Device.objects.get(User=product.uploader)
                send_push_notification(uploader_device.token,f" "+product.name+" has been rejected",message)
            except Device.DoesNotExist:
                print("Device not found")    
            notification=Notifications.objects.create(User=product.uploader,notification_title=f"Product "+ product.name +" has been rejected",notification_body=message,type="Self")
                
            send_mail(
            f'' + product.name +' rejected' ,
            message,
            settings.EMAIL_HOST_USER,
            [product.uploader.email],
            fail_silently=False,
        )    
        except ProductModel.DoesNotExist:
            return JsonResponse({"message":"Product Does not exist"},status=404)  
        product.rejected=True
        product.save()
        return JsonResponse({"message":"Product rejected successfully"})  

        #USER Section
class UserView(View):
    def get(self, request,id=None,*args,**kwargs):
        print(id)
        action=kwargs.get('action')
        
        if action is None:
            if id is not None:
                try:
                    user=User.objects.get(id=id)
                    serializer=UserSerializer(user)
                    return JsonResponse({"user":serializer.data},status=200)
                except User.DoesNotExist:
                    return JsonResponse({"message":"User Does not exist"},status=404)    
               

                
            users=User.objects.all()
            context={"users": users}
            return render(request, "User/users.html",context)     
        if action=='add_new_user':
            form= UserForm()
            return render(request, "User/Add_new_user.html", {"form": form})  
        if action=='edit_user':
            if id is not None:
                user=User.objects.get(id=id)
                form= UserForm(instance=user)
            return render(request, "User/Add_new_user.html", {"form": form,"is_editing":True,"user_id":id})
    def post(self, request, *args, **kwargs):
        if kwargs.get('action')=='add_new_user':
            form=UserForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('users')
        if kwargs.get('action')=='save_edit_user':
            id=request.POST.get('user_id')
            try:
                user=User.objects.get(id=id)
            except User.DoesNotExist:
                return JsonResponse({"message":"User Does not exist"},status=404)    
            form=UserForm(request.POST,request.FILES,instance=user)
            if form.is_valid():
                form.save()
                return redirect('users')    
            return JsonResponse({"message":form.errors}) 


# Shop Class     
class ShopView(View):
    def get(self, request,id=None,*args,**kwargs):
        
        action=kwargs.get('action')
        
        if action is None:
            if id is not None:
                shop=ShopModel.objects.get(id=id)
                products=shop.shop_products()
                
                return render(request,"Shop/single_shop.html",{"shop":shop,"products":products})
            shops=ShopModel.objects.all()
            context={"shops": shops}
            return render(request, "shop/shops.html",context)     
        elif action=='add_new_shop':
            form= ShopForm()
            return render(request, "shop/Add_new_shop.html", {"form": form})  
        elif action=='edit_shop':
            if id is not None:
                shop=ShopModel.objects.get(id=id)
                form= ShopForm(instance=shop)
            return render(request, "shop/Add_new_shop.html", {"form": form,"is_editing":True,"shop_id":id}) 
    def post(self, request, id=None, *args, **kwargs):
        action = kwargs.get('action')
        
        if action == 'save_new_shop':
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('shops')
            else:
                return JsonResponse({"message": form.errors}, status=400)
        
        elif action == 'save_edit_shop':
            id = request.POST.get('shop_id')
            try:
                shop = ShopModel.objects.get(id=id)
            except ShopModel.DoesNotExist:
                return JsonResponse({"message": "Shop does not exist"}, status=404)
            
            form = ShopForm(request.POST, request.FILES, instance=shop)
            if form.is_valid():
                form.save()
                return redirect('shops')
            else:
                return JsonResponse({"message": form.errors}, status=400)
        
        return JsonResponse({"message": "Invalid Action: " + action}, status=400)
class WalletView(View):
    def get(self, request,id=None,*args,**kwargs):
        action=kwargs.get("action")
        if action =='all_transactions':
            all_transactions =WalletHistory.objects.all()  
            paginator = Paginator(all_transactions, 20) 
            page_number = request.GET.get('page')
            transactions = paginator.get_page(page_number) 
            
            print(transactions)
            return render(request,'Wallet/transactions.html',{'transactions': transactions, 'paginator': paginator}) 
        elif action=='search_wallet':
            user=request.GET.get("search")
            wallet=WalletHistory.objects.filter(wallet__user__username__istartswith=user)
            serializer=WalletHistorySerializer(wallet,many=True)
            return JsonResponse({"wallet": serializer.data},status=200)
        HttpClient(client_id="4645d206-48c1-11ef-a6a2-deade826d28d", client_secret="76ff484a244047ecbbc3ffeca5dc79a3da39a3ee5e6b4b0d3255bfef95601890afd80709")
        wallet=Merchant().me()
        events = Event().list()
        print(events)
        return render(request,'Wallet/mywallet.html',{"wallet":wallet,"transactions":events})
    def post(self, request, *args, **kwargs):
        
        action=kwargs.get("action")
        if action=='deposit':
            amount=float(request.POST.get('amount'))
            wallet_id=request.POST.get('wallet_id')
            try:
                wallet=MyWallet.objects.get(id=wallet_id)
                wallet.amount=wallet.amount + amount
                wallet.save()
                return JsonResponse({"message":"Deposit Successful"})
            except Exception as e:
                print(e)
                return JsonResponse({"message":"Error occurred while depositing"},status=500)
        elif action=='withdraw':
            amount=float(request.POST.get('amount'))
            phone_number=request.POST.get('phone_number')
            HttpClient(client_id="4645d206-48c1-11ef-a6a2-deade826d28d", client_secret="76ff484a244047ecbbc3ffeca5dc79a3da39a3ee5e6b4b0d3255bfef95601890afd80709")
            cashout = Transaction().cashout(amount=amount, phone_number=phone_number)
            
            if cashout.get('status'):
                return JsonResponse({"message":"Withdraw Successful"})
            else:
                return JsonResponse({"message":cashout.get('message')},status=200)
        
        return JsonResponse({"message":"Post request"})
def search_function(request):
    query=request.GET.get('search','')
    print("Query",query)
    wallet=MyWallet.objects.filter(user__username__istartswith=query)
    if len(wallet)>0:
        serializer=MyWalletSerializer(wallet,many=True) 
        print(serializer.data)
        return JsonResponse({"result":serializer.data}) 
    else:
        return JsonResponse({"message":"No results found"},status=200)

class RequestView(View):
    def get(self, request,id=None,*args,**kwargs):
        action=kwargs.get('action')
        if action=='approve_request':
            id=request.GET.get('user_id')
            try:
                user=User.objects.get(id=id)
                user.account_status='Verified'
                user.verified=True
                user.save()
                return JsonResponse({"message":"User account approved successfully"})
            except Exception as e:
                print(e)
                return JsonResponse({"message":"Error occurred while approving user account"},status=500)
        elif action == "reject_request":
            id=request.GET.get('user_id')
            print(id)
            try:
                user=User.objects.get(id=id)
                user.account_status='Rejected'
                user.verified=False
                user.save()
                
                return JsonResponse({"message":"User account rejected successfully"})
            except Exception as e:
                print(e)
                return JsonResponse({"message":"Error occurred while rejecting user account"},status=500) 
        elif action =="view_user":
            id=request.GET.get('user_id')
            try:
                user=User.objects.get(id=id)
                serializer=UserSerializer(user)
                return JsonResponse({"user":serializer.data})
            except Exception as e:
                print(e)
                return JsonResponse({"message":"Error occurred while retrieving user"},status=500)       
        all_requests=User.objects.filter(account_status='Pending')
        paginator=Paginator(all_requests,25)
        page_number=request.GET.get('page')
        requests=paginator.get_page(page_number)
        serializer=UserSerializer(all_requests,many=True)
        print(all_requests)
        return render(request,'requests/requests.html',{"requests":requests}) 
         






  