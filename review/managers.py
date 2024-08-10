from django.db import models

from .models import Review


class ReviewManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return Review.objects.filter(content_type=content_type, object_id=obj_id)
