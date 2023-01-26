from django.db import models
from django.utils import timezone

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=200)