from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from upload.models import Document
from accounts.forms import LoginForm
from accounts.models import User
from myprofile.models import Profile
from articles.models import Category
from follow.models import Follow

class HomeView(LoginView):
    authentication_form = LoginForm
    template_name = 'mysite/home.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.annotate(q_count=Count('students')).order_by('-q_count')[:3] # 기본 오름차순, -붙이면 내림차순
        context['Bestdocuments'] = documents

        documents = Document.objects.order_by('-id')[:12] # 특정 모델의 최근 10개 데이터 조회
        context['Newdocuments'] = documents

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

class CategoryView(LoginView):
    authentication_form = LoginForm
    template_name = 'mysite/category.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = self.kwargs.get('pk')
        context['categoryName'] = category
        documents = Document.objects.all().filter(category=Category.objects.get(category=category)).order_by('-id')
        context['documents'] = documents

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

class SearchView(LoginView):
    authentication_form = LoginForm
    template_name = 'mysite/search.html'

    def form_invalid(self, form):
        self.request.method = 'GET'
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = self.kwargs.get('pk')
        context['categoryName'] = category
        documents = Document.objects.all().filter(title__contains=category).order_by('-id')
        print(documents)
        context['documents'] = documents

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