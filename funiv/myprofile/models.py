from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from upload.models import Document

from funiv.storage_backends import PrivateMediaStorage

class Profile(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)
    avator = models.ImageField(null=True, blank=True,)
    profile = models.TextField(blank=False)
    career = models.TextField(blank=False)
    user = models.ForeignKey(get_user_model(), related_name='profiles', on_delete=models.CASCADE, default=None, primary_key=True)