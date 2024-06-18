from .views import MessageView,RoomView
from django.urls import path
urlpatterns = [
    path('<uuid:receiver_id>',MessageView.as_view(),name='chat'),
    path('all_chats',RoomView.as_view(),name='all_chats'),
   
]