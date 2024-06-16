
from django.urls import path
from .views import NewsView


urlpatterns = [
    path('',NewsView.as_view()),
      path('<uuid:news_id>',NewsView.as_view())
    
]
