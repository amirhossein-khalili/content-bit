from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType, Q
from django.db import models

from .managers import ReviewManager


class Review(models.Model):
    objects = ReviewManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    rating = models.IntegerField()

    class Meta:
        unique_together = ("content_type", "user_id", "object_id")
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=5),
                name="rating_range",
            )
        ]

    def __str__(self):
        return f"Review of {self.content_type} by user : {self.user_id}"
