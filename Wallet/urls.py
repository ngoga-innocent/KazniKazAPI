
from django.urls import path
from .views import WalletView,events,Webhook,AdminAccount


urlpatterns = [
    path('',WalletView.as_view(),name='api_wallet'),
    path('events',events),
    path('webhook', Webhook),
    path('admin_account',AdminAccount)
    
]
