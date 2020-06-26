from django.urls import path
from . import views

urlpatterns = [
    path('detail/<pk>/', views.DocumentDetailView.as_view(), name='documentDetail'), #글 자세히
    path('update/<pk>/', views.DocumentUpdateView.as_view(), name='documentUpdate'), #글 수정
    path('addstudent/<pk>/', views.AddUserDocumentRedirectView.as_view(), name='addUserDocument'), #글 수정
]
