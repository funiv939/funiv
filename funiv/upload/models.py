from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from funiv.storage_backends import PrivateMediaStorage
from articles.models import Category



class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    thumbnail = models.ImageField() # ImageField 쓸라면 Pillow 설치해야함
    user = models.ForeignKey(get_user_model(), related_name='documents', on_delete=models.DO_NOTHING, default=None, null=True)
    students = models.ManyToManyField(get_user_model(), related_name='students')
    category = models.ForeignKey(Category, related_name='documentsCategory', on_delete=models.DO_NOTHING, default=None, null=True) # 원래는 Not Null로 할려고했는데 참조할 수 있는 번호가 없어서 오류 뜨더라...ㅠ

    @property
    def total_student(self):
        return self.student.count() #follow 컬럼의 값의 갯수를 센다

class PrivateDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage())
    user = models.ForeignKey(get_user_model(), related_name='documentsPrivate', on_delete=models.DO_NOTHING, default=None, null=True)