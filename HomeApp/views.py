from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from Product.models import Category,ProductModel,OurAds
from django.db.models import Q
from Account.firebase import send_push_notification
import os
from django.conf import settings
from django.http import HttpResponse
# Create your views here.
class HomeView(View):
    def get(self, request,pk=None):
        if pk is not None:
            product=ProductModel.objects.get(pk=pk)
            context={'product': product}
            return render(request, 'ProductPage.html',context)
        
        
        categories = Category.objects.filter(parent=None).order_by('name')
        new_product=ProductModel.objects.filter(Q(place='admin') | Q(discount__gte=0)).order_by('-created_at')[:12]
        our_ads=OurAds.objects.all()
        context={'categories': categories,'new_products': new_product,'our_ads': our_ads}
        return render(request, 'Homepage.html',context)
class ProductView(View):
    def get(self, request):
        products=ProductModel.objects.all().order_by('-created_at')
        context={'products': products}
        return render(request, 'Products/products.html',context)    
class AboutUsView(View):
    def get(self, request):
        return render(request, 'AboutUs.html')    
def serve_assetlinks_json(request):
    assetlinks_json_path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(assetlinks_json_path, 'r') as file:
        return HttpResponse(file.read(), content_type='application/json')   
def Privacy(request):
    return render(request, 'Privacy.html')     
