
from django.urls import path
from .views import Register,Login,LogoutView,UserProfile,DeviceRegister,NotificationView,WebSignup,request_verification,checkOtp,GenerateOTPView,ResetPasswordView


urlpatterns = [
    path('register', Register.as_view(),name='app_register'),
    path('login', Login.as_view(),name='app_login'),
    path('register_token',DeviceRegister.as_view(),name='device_register_token'),
    path('logout',LogoutView.as_view()),
    path('profile',UserProfile.as_view()),
    path('notification',NotificationView.as_view()),
    path('Login',WebSignup.as_view(),name='web_signup'),
    path("request_Verification",request_verification,name='request_verification'),
    path("otp_request",GenerateOTPView.as_view(),name='otp_request'),
    path("check_otp",checkOtp.as_view(),name='verify_otp'),
    path("reset_password",ResetPasswordView.as_view(),name='reset_password')
    
]
