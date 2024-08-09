from django.db import models


class Article(models.Model):
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    # )

    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=20, default=None)

    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
