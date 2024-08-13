from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType, Q
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

from .managers import ReviewManager


class Review(models.Model):
    """
    this model for now is only used for

    just in the article . there is some field and options

    to if this model wants to used in multiple places

    you can use generic relation .

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    article = models.ForeignKey(
        "content.Article",
        related_name="reviews",
        on_delete=models.CASCADE,
    )

    rating = models.IntegerField()

    class Meta:
        unique_together = ("user_id", "article_id")
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=5),
                name="rating_range",
            )
        ]

    def __str__(self):
        return f"Review of article {self.article_id} by user {self.user_id}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    review_count = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


# class Review(models.Model):

#     # objects = ReviewManager()
#     # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     # object_id = models.PositiveIntegerField()
#     # content_object = GenericForeignKey()

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         unique=True,
#     )

#     # this field is saved as foreign key
#     # It is because we do not have another model that is related to Review
#     # In the future, if you need to use it in other places, you can use it used generic fields
#     article = models.ForeignKey(
#         "content.Article",
#         related_name="reviews",
#         on_delete=models.CASCADE,
#     )

#     rating = models.IntegerField()

#     class Meta:
#         # unique_together = ("content_type", "user_id", "object_id")
#         unique_together = ("user_id", "article_id")
#         constraints = [
#             models.CheckConstraint(
#                 check=Q(rating__gte=0) & Q(rating__lte=5),
#                 name="rating_range",
#             )
#         ]

#     def __str__(self):
#         return f"Review of {self.content_type} by user : {self.user_id}"
