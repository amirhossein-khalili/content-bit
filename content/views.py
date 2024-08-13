from django.db.models import Avg, OuterRef, Subquery
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
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


class ReviewCreateUpdateView(APIView):
    """
    This part allows users to give a score to an article.
    if user had been scored before it will be update .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request, pk):

        # check article exists with slug
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404("مقاله مد نظر شما وجود ندارد . ")

        # serialize data input of user
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "article": article},
        )

        # check validation and error messages .
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "امتیاز شما با موفقیت ثبت شد ."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
