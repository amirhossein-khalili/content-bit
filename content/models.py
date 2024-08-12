from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify

from review.models import Review


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
