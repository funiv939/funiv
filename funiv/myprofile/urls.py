from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('update/<pk>/', views.ProfileUpdateView.as_view(), name='profileUpdate'),
    path('detail/<pk>/', views.ProfileView.as_view(), name='profile'),
]
