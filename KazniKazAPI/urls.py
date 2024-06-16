from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls,name='register'),
    path('account/',include('Account.urls')),
    path('product/',include('Product.urls')),
    path('wallet/',include('Wallet.urls')),
    path('jobs/',include('Jobs.urls')),
    path('news/',include('News.urls')),
    path('chat/',include('Chat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)