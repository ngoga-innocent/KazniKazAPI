
from django.urls import path
from .views import HomeView,AboutUsView,serve_assetlinks_json,Privacy,ProductView


urlpatterns = [
    path('',HomeView.as_view(),name='homepage'),
    path('about',AboutUsView.as_view(),name='about_us'),
    path('single_product/<uuid:pk>',HomeView.as_view(),name='single_product'),
    path('.well-known/assetlinks.json', serve_assetlinks_json, name='assetlinks-json'),
    path('privacy',Privacy,name='privacy'),
    path('products',ProductView.as_view(),name='products'),
      
]
