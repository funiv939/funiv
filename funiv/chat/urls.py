from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns = [
    
    path('', views.ChatView.as_view(), name='chat'), 

    path('<room_name>/', views.room, name='room'), # 채팅
    path('group/<pk>/', views.messageGroup, name='messageGroup'),
]