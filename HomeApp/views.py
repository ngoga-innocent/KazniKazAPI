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
        token="e2cxTDGXR3KwvlixkpWQF5:APA91bHPUt5t8I821qDCmr9ADECz6ZWNewgNQuP4i3aHc60yPVg4gdGakEd6dGuAILQCqK_a8Ai-xU_Z7LB1U4unJLwApysvpgQ5p0lo1o1Dad7zsFWM1uy6UaH-kdDmO_08hMOL_aW9"
        notification=send_push_notification(token, 'Kaz ni Kaz Api checking notification', 'Description of Fcm notifications')
        print(notification)
        categories = Category.objects.filter(parent=None).order_by('name')
        new_product=ProductModel.objects.filter(Q(place='admin') | Q(discount__gte=0)).order_by('-created_at')[:12]
        our_ads=OurAds.objects.all()
        context={'categories': categories,'new_products': new_product,'our_ads': our_ads}
        return render(request, 'Homepage.html',context)
class AboutUsView(View):
    def get(self, request):
        return render(request, 'AboutUs.html')    
def serve_assetlinks_json(request):
    assetlinks_json_path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(assetlinks_json_path, 'r') as file:
        return HttpResponse(file.read(), content_type='application/json')   
def Privacy(request):
    return render(request, 'Privacy.html')     