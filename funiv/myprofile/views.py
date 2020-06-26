from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect

from .models import Profile
from .forms import ProfileUpdateForm
from upload.models import Document
from follow.models import Follow

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    context_object_name = 'profile'
    template_name = 'myprofile/profile_form.html'
    pk_url_kwarg = 'pk'
    
    def get(self, request, **kwargs):
        self.model.objects.get(pk=kwargs['pk'])
        return super().get(request, **kwargs)

    def form_valid(self, form):
        Profile = form.save(commit=False)
        Profile.updated_at = timezone.now()
        Profile.save()
        return redirect('profile', pk=Profile.pk)

class ProfileView(DetailView):
    model = Profile # 모델을 settings.py에서 자동으로 가져옴
    context_object_name = 'profile' # 디폴트 컨텍스트 변수명 :  object
    template_name = 'myprofile/profile.html'
    
    def get(self, request, **kwargs):
        try:
            self.model.objects.get(pk=kwargs['pk'])
            return super().get(request, **kwargs)
        except self.model.DoesNotExist:
            return redirect(reverse_lazy('profileUpdate'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all().filter(user_id = self.kwargs.get('pk')).order_by('-id')
        context['Mydocuments'] = documents

        documents = Document.objects.all().filter(students = self.kwargs.get('pk'))
        context['Listendocuments'] = documents
        
        try :
            follows = Follow.objects.get(user=self.request.user.pk)
            user = self.kwargs.get('pk')
            if follows.followings.filter(pk=user).exists(): #이미 해당 유저가 students컬럼 존재하면
                context['exist'] = True
            else:
                context['exist'] = False
        except Follow.DoesNotExist :
            context['exist'] = False
            
        return context

