from django.urls import path
from . import views

urlpatterns = [
    path('public/', views.DocumentCreateView.as_view(), name='upload'), #공개 파일 업로드
    path('private/', views.PrivateDocumentCreateView.as_view(), name='uploadPrivate'), #비공개 파일 업로드
]