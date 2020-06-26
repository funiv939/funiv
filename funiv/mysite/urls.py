from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), #메인화면
    path('category/<pk>/', views.CategoryView.as_view(), name='category'),
    path('search/<pk>/', views.SearchView.as_view(), name='search'),
]
