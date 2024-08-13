from django.db.models import Avg, OuterRef, Subquery
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Review
from .serializers import ArticleSerializer, ReviewCreateSerializer


class ArticleListView(ListAPIView):
    """
    Returns a paginated list of articles with the user's rating for each article
    and the average rating for all articles. The page number must be sent in query parameters.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        # Annotate queryset with user-specific rating

        return Article.objects.annotate(
            user_rating=Subquery(
                Review.objects.filter(article=OuterRef("pk"), user=user).values(
                    "rating"
                )[:1]
            ),
        )


class ArticleMixin:
    """Mixin to retrieve an article instance based on pk"""

    def get_article(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404("مقاله مد نظر شما وجود ندارد .")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["article"] = self.article
        return context


class ReviewCreateUpdateView(ArticleMixin, CreateAPIView):
    """
    Allows users to give a score to an article.
    If the user has already scored, it will be updated.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request, pk, *args, **kwargs):
        # Retrieve the article using the mixin
        self.article = self.get_article(pk)

        # Use the inherited method to handle serialization and saving
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article=self.article)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "امتیاز شما با موفقیت ثبت شد"},
            status=status.HTTP_200_OK,
        )
