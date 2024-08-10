from django.db.models import Avg, OuterRef, Subquery
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review

from .models import Article
from .serializers import ArticleSerializer


class ArticleListView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer

    def get(self, request):
        user = request.user

        # Annotate each article with the average rating
        articles = Article.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            user_rating=Subquery(
                Review.objects.filter(
                    content_type=OuterRef("reviews__content_type"),
                    object_id=OuterRef("id"),
                    user=user,
                ).values("rating")[:1]
            ),
        )
        serializer = self.serializer_class(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
