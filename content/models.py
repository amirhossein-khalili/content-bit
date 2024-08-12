from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify

from review.models import Review


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    reviews = GenericRelation(Review, related_query_name="article")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:5]
            counter = 1
            original_slug = self.slug
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
