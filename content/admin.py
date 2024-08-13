from django.contrib import admin

from .models import Article, Review


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
