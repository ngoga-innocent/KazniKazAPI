
from django.urls import path
from .views import ProductView,CategoryView,ColorViews,filter_products,ShopView,UserShops,FeatureView,OurAdsView,VipProduct


urlpatterns = [
    path('', ProductView.as_view()),
    path('categories',CategoryView.as_view()),
    path('colors',ColorViews.as_view()),
    path('shop',ShopView.as_view()),
    path('shop/<uuid:shop_id>',ShopView.as_view()),
    path('user_shops',UserShops.as_view()),
    path('category_features',FeatureView.as_view()),
    path('category_features/<uuid:category_id>',FeatureView.as_view()),
    path('our_ads',OurAdsView.as_view(),name='our_ads'),
    path('vips',VipProduct.as_view(),name='vips'),
    path('filter',filter_products.as_view(),name='filter'),
    
    
]
