
from django.urls import path
from .views import Register,Login,LogoutView,UserProfile,DeviceRegister,NotificationView,WebSignup


urlpatterns = [
    path('register', Register.as_view(),name='app_register'),
    path('login', Login.as_view(),name='app_login'),
    path('register_token',DeviceRegister.as_view(),name='device_register_token'),
    path('logout',LogoutView.as_view()),
    path('profile',UserProfile.as_view()),
    path('notification',NotificationView.as_view()),
    path('Login',WebSignup.as_view(),name='web_signup'),
    
]
