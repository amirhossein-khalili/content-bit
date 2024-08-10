from django.db import connection
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    user_rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "published_date",
            "updated_date",
            "avg_rating",
            "user_rating",
        ]

    def get_avg_rating(self, obj):
        return obj.avg_rating if obj.avg_rating is not None else 0
