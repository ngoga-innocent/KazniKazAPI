from .views import MessageView
from django.urls import path
urlpatterns = [
    path('<uuid:receiver_id>',MessageView.as_view(),name='chat')
]