
from django.urls import path
from .views import ProductView,CategoryView,ColorViews


urlpatterns = [
    path('', ProductView.as_view(),name='register'),
    path('categories',CategoryView.as_view()),
    path('colors',ColorViews.as_view())
    
]
