from django.shortcuts import render
from django.views.generic import RedirectView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Follow
from accounts.models import User
from accounts.forms import LoginForm
from myprofile.models import Profile
from articles.models import Category

class AddFollowRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'profile'

    def get_redirect_url(self, *args, **kwargs):
        try :
            user = self.request.user.pk
            user_follow = Profile.objects.get(pk=kwargs['pk'])
            follows = Follow.objects.get(user=user)
            if follows.followings.filter(pk=user_follow.pk).exists(): #이미 해당 유저가 students컬럼 존재하면
                follows.followings.remove(user_follow) #students 컬럼에서 해당 유저를 지운다.
            else:
                follows.followings.add(user_follow)
            return super().get_redirect_url(*args, **kwargs)
        except TypeError :
            self.pattern_name = 'login'
            messages.error(self.request, '로그인 해주세요.')
            return super().get_redirect_url(*args, **kwargs)


class FollowingView(LoginRequiredMixin, LoginView):
    authentication_form = LoginForm
    template_name = 'follow/following.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorys = Category.objects.all()
        context['categorys'] = categorys

        try:
            profile = Profile.objects.get(pk=self.request.user.pk)
            context['myprofile'] = profile
            follows = Follow.objects.get(user=self.request.user.pk)
            context['follows'] = follows
            context['followings'] = follows.followings.all()
            followers = Follow.objects.filter(followings=self.request.user.pk)
            context['follower'] = followers
        except ObjectDoesNotExist:
            profile = None
            
        return context


class FollowerView(LoginRequiredMixin, LoginView):
    authentication_form = LoginForm
    template_name = 'follow/follower.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorys = Category.objects.all()
        context['categorys'] = categorys

        try:
            profile = Profile.objects.get(pk=self.request.user.pk)
            context['myprofile'] = profile
            follows = Follow.objects.get(user=self.request.user.pk)
            context['follows'] = follows
            followers = Follow.objects.filter(followings=self.request.user.pk)
            context['follower'] = followers
            context['followers'] = followers
            print(followers)
        except ObjectDoesNotExist:
            profile = None
        except TypeError:
            profile = None
            
        return context