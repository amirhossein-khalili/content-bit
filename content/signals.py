from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Article, Review


@receiver(post_save, sender=Review)
def handle_review_save(sender, instance, created, **kwargs):

    article = instance.article
    new_rating = instance.rating
    review_count = article.review_count

    if created:

        # calculate and update average of rating of this article
        new_review_avg = ((review_count * article.avg_rating) + (new_rating)) / (
            review_count + 1
        )
        article.avg_rating = new_review_avg

        # Increase the review_count for the associated article
        article.review_count += 1
        article.save()

    else:

        # Retrieve the previous rating
        previous_rating = Review.objects.get(pk=instance.pk).rating

        # Calculate the updated average after changing the rating
        new_review_avg = (
            (review_count * article.avg_rating) - previous_rating + new_rating
        ) / review_count

        # Update the article's average rating
        article.avg_rating = new_review_avg
        article.save()


@receiver(post_delete, sender=Review)
def handle_review_save(sender, instance, **kwargs):

    article = instance.article
    article.review_count -= 1
    article.save()
