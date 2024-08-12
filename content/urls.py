from django.urls import include, path

from . import views

app_name = "content"
urlpatterns = [
    path("list/", views.ArticleListView.as_view()),
    path(
        "<slug:article_slug>/review/",
        views.ReviewArticleCreateUpdateView.as_view(),
    ),
]
