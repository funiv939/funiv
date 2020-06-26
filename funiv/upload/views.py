from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Document, PrivateDocument


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['category', 'title', 'content', 'upload', 'thumbnail', ]
    success_url = reverse_lazy('home')
    template_name = 'upload/upload_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all()
        context['documents'] = documents
        return context

class PrivateDocumentCreateView(LoginRequiredMixin, CreateView):
    model = PrivateDocument
    fields = ['upload', 'user']
    success_url = reverse_lazy('home')
    template_name = 'upload/upload_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = PrivateDocument.objects.all()
        context['documents'] = documents
        return context