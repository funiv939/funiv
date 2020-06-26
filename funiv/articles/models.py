from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self): return self.category