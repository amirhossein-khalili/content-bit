from django.contrib.contenttypes.models import ContentType
from django.db import connection
from rest_framework import serializers

from review.models import Review

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
            "published_date",
            "updated_date",
            "avg_rating",
            "user_rating",
        ]

    def get_avg_rating(self, obj):
        return obj.avg_rating if obj.avg_rating is not None else 0


class ReviewCreateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        min_value=0,
        max_value=5,
        write_only=True,
        error_messages={
            "required": "ارسال مقدار امتیاز اجباری هست",
            "blank": "ارسال مقدار امتیاز اجباری هست",
            "min_value": "حداقل مقدار امتیاز میتواند عدد ۰ باشد ",
            "max_value": "حداکثر مقدار امتیاز میتواند عدد ۵ باشد ",
            "invalid": "مقدار امتیاز باید یک عدد باشد ",
        },
    )

    class Meta:
        model = Review
        fields = ["rating"]

    def create(self, validated_data):
        user = self.context["request"].user
        article = self.context["article"]

        review, created = Review.objects.update_or_create(
            user=user,
            article=article,
            defaults={"rating": validated_data["rating"]},
        )

        return review
