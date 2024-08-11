from django.db.models import Avg, OuterRef, Subquery
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review

from .models import Article
from .serializers import ArticleSerializer, ReviewCreateSerializer

# class ArticleListView(APIView):

#     permission_classes = [IsAuthenticated]
#     serializer_class = ArticleSerializer

#     def get(self, request):
#         user = request.user

#         # Annotate each article with the average rating
#         articles = Article.objects.annotate(
#             avg_rating=Avg("reviews__rating"),
#             user_rating=Subquery(
#                 Review.objects.filter(
#                     content_type=OuterRef("reviews__content_type"),
#                     object_id=OuterRef("id"),
#                     user=user,
#                 ).values("rating")[:1]
#             ),
#         )
#         serializer = self.serializer_class(articles, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


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

        # Set up pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of articles per page
        paginated_articles = paginator.paginate_queryset(articles, request)

        # Serialize the data
        serializer = self.serializer_class(paginated_articles, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class AddArticleRatingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request, article_id):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response(
                {"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "article": article},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
