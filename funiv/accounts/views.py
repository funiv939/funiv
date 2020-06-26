from django.shortcuts import render, redirect
# from .models import User
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, LoginForm, VerificationEmailForm
from .mixins import VerifyEmailMixin
from upload.models import Document
from myprofile.models import Profile
from follow.models import Follow

class UserRegistrationView(VerifyEmailMixin, CreateView):
    # model = User                            # 자동생성 폼에서 사용할 모델
    # fields = ('email', 'name', 'password')  # 자동생성 폼에서 사용할 필드
    model = get_user_model() # 모델을 settings.py에서 자동으로 가져옴
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    verify_url = reverse_lazy('verifyEmail')
    template_name = 'accounts/signup_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)

class UserVerificationView(TemplateView):

    model = get_user_model()
    redirect_success_url = reverse_lazy('login')
    redirect_fail_url = reverse_lazy('verifyEmailRetry')
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
            Profile.objects.create(avator='no-avatar.gif', profile="자기소개 입니다. 작성해주세요.", career="경력 입니다. 작성해주세요", user=self.model.objects.get(pk=kwargs.get('pk')))
            Follow.objects.create(user=Profile.objects.get(pk=kwargs.get('pk')))
            return HttpResponseRedirect(self.redirect_success_url) # 인증 성공시 로그인 화면으로
        else:
            messages.error(request, '인증이 실패되었습니다.')
            return HttpResponseRedirect(self.redirect_fail_url) # 인증 실패시 재발송 화면으로

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()     # 데이터가 변경되면 반드시 save() 메소드 호출
        return is_valid

class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/resend_verify_form.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)