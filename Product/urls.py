
from django.urls import path
from .views import ProductView,CategoryView,ColorViews,ShopView,UserShops


urlpatterns = [
    path('', ProductView.as_view(),name='register'),
    path('categories',CategoryView.as_view()),
    path('colors',ColorViews.as_view()),
    path('shop',ShopView.as_view()),
    path('shop/<uuid:shop_id>',ShopView.as_view()),
    path('user_shops',UserShops.as_view())
    
]
