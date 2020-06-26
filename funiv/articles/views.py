from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.views.generic import RedirectView
from django.urls import reverse
from django.contrib.auth.views import LoginView

from upload.models import Document
from .forms import DocumentUpdateForm
from articles.models import Category
from myprofile.models import Profile
from accounts.forms import LoginForm

class DocumentDetailView(DetailView):
    model = Document # 모델을 settings.py에서 자동으로 가져옴
    context_object_name = 'document' # 디폴트 컨텍스트 변수명 :  object
    template_name = 'articles/document.html'
    
    def get(self, request, **kwargs):
        try:
            self.model.objects.get(pk=kwargs['pk'])
            return super().get(request, **kwargs)
        except self.model.DoesNotExist:
            return redirect(reverse_lazy('home'))
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categorys = Category.objects.all()
        context['categorys'] = categorys
        
        document = Document.objects.get(pk=self.kwargs.get('pk'))
        user = self.request.user
        if document.students.filter(id=user.pk).exists(): #이미 해당 유저가 students컬럼 존재하면
            context['exist'] = True
        else:
            context['exist'] = False

        try:
            profile = Profile.objects.get(pk=document.user.pk)
            context['documentprofile'] = profile
            profile = Profile.objects.get(pk=self.request.user.pk)
            context['myprofile'] = profile
        except Profile.DoesNotExist:
            profile = None
            
        return context

class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentUpdateForm
    context_object_name = 'document'
    template_name = 'articles/document_form.html'
    pk_url_kwarg = 'pk'
    
    def get(self, request, **kwargs):
        self.model.objects.get(pk=kwargs['pk'])
        return super().get(request, **kwargs)

    def form_valid(self, form):
        Profile = form.save(commit=False)
        Profile.uploaded_at = timezone.now()
        Profile.save()
        return redirect('profile', pk=Profile.pk)


class AddUserDocumentRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'documentDetail'

    def get_redirect_url(self, *args, **kwargs):
        document = Document.objects.get(pk=kwargs['pk'])
        user = self.request.user
        if document.students.filter(id=user.pk).exists(): #이미 해당 유저가 students컬럼 존재하면
            document.students.remove(user) #students 컬럼에서 해당 유저를 지운다.
        else:
            document.students.add(user)
        return super().get_redirect_url(*args, **kwargs)