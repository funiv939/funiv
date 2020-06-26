from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.UserRegistrationView.as_view(), name='signup'), #회원가입
    path('login/', views.UserLoginView.as_view(), name='login'), # 로그인
    path('login/<pk>/', views.UserLoginView.as_view(), name='login'), # 로그인
    path('logout/', LogoutView.as_view(), name='logout'), # 로그아웃
    path('<pk>/verify/<token>/', views.UserVerificationView.as_view(), name='verifyEmail'), # 이메일 인증
    path('resend_verify_email/', views.ResendVerifyEmailView.as_view(), name='verifyEmailRetry'), # 이메일 재발송

]
