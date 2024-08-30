from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from HomeApp.views import LoginView,RegisterView
urlpatterns = [
    path('admin/', admin.site.urls,name='register'),
    path('login/', LoginView.as_view(), {"action":"login"}, name='login'),
    path('register/', RegisterView.as_view(), {"action":"register"}, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/',include('Account.urls')),
    path('product/',include('Product.urls')),
    path('wallet/',include('Wallet.urls')),
    path('jobs/',include('Jobs.urls')),
    path('news/',include('News.urls')),
    path('chat/',include('Chat.urls')),
    path('',include('HomeApp.urls')),
    path('staff/',include('Staff.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)