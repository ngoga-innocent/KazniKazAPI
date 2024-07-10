
from django.urls import path
from .views import Register,Login,LogoutView,UserProfile,DeviceRegister,NotificationView


urlpatterns = [
    path('register', Register.as_view(),name='register'),
    path('login', Login.as_view(),name='login'),
    path('register_token',DeviceRegister.as_view(),name='device_register_token'),
    path('logout',LogoutView.as_view()),
    path('profile',UserProfile.as_view()),
    path('notification',NotificationView.as_view()),
    
]
