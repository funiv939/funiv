from django.db import models
from django.contrib.auth import get_user_model

from myprofile.models import Profile

class Follow(models.Model):
    user = models.ForeignKey(Profile, related_name='followFrom', on_delete=models.CASCADE, default=None, unique=True)
    followings = models.ManyToManyField(Profile, related_name='follows')

    @property
    def total_following(self):
        return self.followings.count() #follow 컬럼의 값의 갯수를 센다

    # def __str__(self):
    #     return self.user.name