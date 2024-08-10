from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from review.models import Review


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=20, default=None)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    reviews = GenericRelation(Review, related_query_name="article")

    def __str__(self):
        return self.title
