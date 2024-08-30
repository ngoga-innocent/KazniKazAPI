
from django.urls import path
from .views import Home,product_sales_data,CategoryStaff,AddCategoryFeatures,AddCategoryView,ProductViewStaff,WalletView,get_product_by_type,RequestView,rejectProduct,UserView,ShopView,search_function


urlpatterns = [
    path('',Home.as_view(),name='staff_home'),
    path('product-sales',product_sales_data,name='product_sales'),
    path('categories',CategoryStaff.as_view(),name='category_staff'),
    path('categories/<uuid:category_id>',CategoryStaff.as_view(),name='category_staff'),
    path('addCategory',AddCategoryView.as_view(),name='addCategory'),
    path('category_features',AddCategoryFeatures.as_view(),name='category_features'),
    path('product',ProductViewStaff.as_view(),name='products'),
    path('product/<uuid:product_id>',ProductViewStaff.as_view(),name='product_edit'),
    path('product_form',ProductViewStaff.as_view(),{'action':'get_form'},name='get_form'),
    path('product_form/<uuid:product_id>',ProductViewStaff.as_view(),{'action':'get_edit_form'},name='get_edit_form'),
    path('products_by_type',get_product_by_type,name='get_products_by_type'),
    path('reject_product',rejectProduct.as_view(),name='reject_product'),
    # User Urls
    path('users',UserView.as_view(),name='users'),
    path('user/<uuid:id>',UserView.as_view(),name='user'),
    # Add new user and save edited user Urls
    path('add_users',UserView.as_view(),{'action':'add_new_user'},name='add_new_user'),
    path('save_user',UserView.as_view(),{'action':'add_new_user'},name='save_user'),
    path('edit_user/<uuid:id>',UserView.as_view(),{'action':"edit_user"},name='edit_users'),
    path('save_edited_user',UserView.as_view(),{'action':"save_edit_user"},name='save_edited_user'),

    # Shops Urls
    path('shops',ShopView.as_view(),name='shops'),
    path('shop/<uuid:id>',ShopView.as_view(),name='shop'),
    path('add_shops',ShopView.as_view(),{"action":"add_new_shop"},name='add_new_shop'),
    path('edit_shops/<uuid:id>',ShopView.as_view(),{"action":"edit_shop"},name='edit_shop'),
    path('save_new_shop',ShopView.as_view(),{"action":"save_new_shop"},name='save_new_shop'),
    path('edit_shop',ShopView.as_view(),{"action":"save_edit_shop"},name='save_edit_shop'),

    # Wallet Urls
    path('wallet',WalletView.as_view(),name='wallet'),
    path('search_user',search_function,name='search_user'),
    path("staff_deposit",WalletView.as_view(),{"action":"deposit"},name='staff_deposit'),
    path("staff_withdraw",WalletView.as_view(),{"action":"withdraw"},name='staff_withdraw'),
    path("all_transactions",WalletView.as_view(),{"action":"all_transactions"},name='all_transactions'),
    path("search_wallet",WalletView.as_view(),{"action":"search_wallet"},name='search_wallet'),

    # Request Urls
    path("all_requests",RequestView.as_view(),name='all_requests'),
    path('view_user',RequestView.as_view(),{"action":"view_user"},name='view_user'),
    path("approve_request",RequestView.as_view(),{"action":"approve_request"},name='approve_request'),
    path("reject_request",RequestView.as_view(),{"action":"reject_request"},name='reject_request'),
    

]
