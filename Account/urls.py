
from django.urls import path
from .views import Register,Login,LogoutView,UserProfile


urlpatterns = [
    path('register', Register.as_view(),name='register'),
    path('login', Login.as_view(),name='login'),
    path('logout',LogoutView.as_view()),
    path('profile',UserProfile.as_view())
    
]
