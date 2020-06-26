from django.urls import path
from . import views

urlpatterns = [
    path('follow/<pk>/', views.AddFollowRedirectView.as_view(), name='follow'),
    path('followinglist/', views.FollowingView.as_view(), name='followingList'),
    path('followerlist/', views.FollowerView.as_view(), name='followerList'),
]
