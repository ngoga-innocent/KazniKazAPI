
from django.urls import path
from .views import HomeView,AboutUsView,serve_assetlinks_json,Privacy,ProductView,CategoryView,ShopView,categorychildren


urlpatterns = [
    path('',HomeView.as_view(),name='homepage'),
    path('about',AboutUsView.as_view(),name='about_us'),
    path('single_product/<uuid:id>',ProductView.as_view(),name='single_product'),
    path('.well-known/assetlinks.json', serve_assetlinks_json, name='assetlinks-json'),
    path('privacy',Privacy,name='privacy'),
    path('products',ProductView.as_view(),name='web_products'),
    path('add_product',ProductView.as_view(),{"action":"upload_product"},name='upload_products'),
    path('product/category/<uuid:id>',CategoryView.as_view(),name='category'),
    path("shops",ShopView.as_view(),name='web_shops'),
    path("addshops",ShopView.as_view(),{"action":"new_shop"},name='add_shop'),
    path("shops/<uuid:id>",ShopView.as_view(),{"action":"shop_category"},name='shop_category'),
    path("shop/<uuid:id>",ShopView.as_view(),{"action":"shop_details"},name='shop_details'),
    path('search_shop',ShopView.as_view(),{"action":"search"},name='search_shop'),
    path('getchildren',categorychildren,name='getchildren'),
    
      
]
