from django.db import models

from .models import Review


class ReviewManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return Review.objects.filter(content_type=content_type, object_id=obj_id)

    def create_review(self, user, content_object, rating):

        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")

        content_type = ContentType.objects.get_for_model(content_object)

        review = self.create(
            user=user,
            content_type=content_type,
            object_id=content_object.pk,
            rating=rating,
        )
        return review
