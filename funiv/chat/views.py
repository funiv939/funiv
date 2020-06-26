from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import MessageGroup
from accounts.forms import LoginForm
from myprofile.models import Profile
from articles.models import Category
from follow.models import Follow

import json

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username' : mark_safe(json.dumps(request.user.name)),
    })

@login_required
def messageGroup(request, pk):
    exist = MessageGroup.objects.filter(Q(user=get_user_model().objects.get(pk=pk), friend=request.user) | Q(user=request.user, friend=get_user_model().objects.get(pk=pk)))
    if len(exist) == 0:
        MessageGroup.objects.create(user=request.user , friend=get_user_model().objects.get(pk=pk))

    return redirect(reverse('chat'))

class ChatView(LoginRequiredMixin, LoginView):
    authentication_form = LoginForm
    template_name = 'chat/index.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        chatlists = MessageGroup.objects.filter(Q(friend=self.request.user) | Q(user=self.request.user))
        context['chatlists'] = chatlists

        categorys = Category.objects.all()
        context['categorys'] = categorys

        try:
            profile = Profile.objects.get(pk=self.request.user.pk)
            context['myprofile'] = profile
            follows = Follow.objects.get(user=self.request.user.pk)
            context['follows'] = follows
            followers = Follow.objects.filter(followings=self.request.user.pk)
            context['follower'] = followers
        except ObjectDoesNotExist:
            profile = None
            
        return context