
from django.urls import path
from .views import HomeView,AboutUsView,serve_assetlinks_json,Privacy,load_messages,JobSearch,load_room,ProductView,SearchProduct,FilterProduct,filterProductByMinandMax,CategoryView,ShopView,categorychildren,ForgotPassword,ChatView,JobView,JobFilter,JobPost,NewsView,WalletWeb,Notification,requestVerification


urlpatterns = [
    path('',HomeView.as_view(),name='homepage'),
    path('about',AboutUsView.as_view(),name='about_us'),
    path('single_product/<uuid:id>',ProductView.as_view(),name='single_product'),
    path('.well-known/assetlinks.json', serve_assetlinks_json, name='assetlinks-json'),
    path('privacy',Privacy,name='privacy'),
    # Product
    path('products',ProductView.as_view(),name='web_products'),
    path('add_product',ProductView.as_view(),{"action":"upload_product"},name='upload_products'),
    path('product/category/<uuid:id>',CategoryView.as_view(),name='category'),
    path('product/filter_products',FilterProduct,name='filter_product'),
    path('product/minmaxfilter',filterProductByMinandMax,name='minmax_filter'),
    path('search_product',SearchProduct,name='search_product'),
    # Shops
    path("shops",ShopView.as_view(),name='web_shops'),
    path("addshops",ShopView.as_view(),{"action":"new_shop"},name='add_shop'),
    path("shops/<uuid:id>",ShopView.as_view(),{"action":"shop_category"},name='shop_category'),
    path("shop/<uuid:id>",ShopView.as_view(),{"action":"shop_details"},name='shop_details'),
    path('search_shop',ShopView.as_view(),{"action":"search"},name='search_shop'),
    path('getchildren',categorychildren,name='getchildren'),
    path('forgot_password',ForgotPassword.as_view(),name='reset_password_page'),
    
    # //Chat Urls
    path('chats/<uuid:uploader_id>',ChatView.as_view(),name='chat'),
     path('kaz_ni_kaz_chats/',ChatView.as_view(),name='chatss'),
    path('kaz_ni_kaz_chat',ChatView.as_view(),name='normal_chat'),
    path('user_chat/',ChatView.as_view(),name='chats'),
    path('load_messages/', load_messages, name='load_messages'),
    path('load_room/', load_room, name='load_rooms'),
    
    # JOBS URL
    path('jobs', JobView.as_view(),name="jobs"),
    path('job_detail/<uuid:id>', JobView.as_view(),name="jobs_details"),
    path('filter_job',JobFilter,name="filter_job"),
    path('search_job',JobSearch,name="filter_job_search"),
    path('post_job',JobPost,name="post_job"),
    
#    News URL
    path('kaz_ni_kaz_news', NewsView.as_view(),name="kaz_news"),
    
#    path('news_tags/<uuid:id>', NewsView.as_view(),name="news_tags"),
    path('mywallet',WalletWeb.as_view(),name="mywallet"),
    
    # Notification
    path('notifications', Notification.as_view(),{"action":"count_not"}, name='get_notification'),
    path('getnotification', Notification.as_view(),name='get_notifications'),
    path('verify',requestVerification.as_view(),name='verify')
    
      
]
