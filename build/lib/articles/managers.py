import datetime

from django.conf import settings
from django.db import models

RESTRICT_CONTENT_TO_SITE = getattr(settings, 'RESTRICT_CONTENT_TO_SITE', False)


class DestinationManager(models.Manager):
    """ Limits to active destination assignments. """
    def get_queryset(self):
        return super(DestinationManager, self).get_queryset().filter(active=True)


class BlogManager(models.Manager):
    """
    Limits to active destination assignments
    and assignments that are marked as Blogs.
    """
    def get_queryset(self):
        blogs = super(BlogManager, self).get_queryset()
        blogs.filter(active=True, is_blog=True)
        return blogs


class ArticlesManager(models.Manager):
    """
    Custom article objects manager.
    If RESTRICT_CONTENT_TO_SITE is True in settings,
    will limit articles to current site.

    Usage is simply article.objects.all()
    """
    def get_queryset(self):
        articles = super(ArticlesManager, self).get_queryset()
        if RESTRICT_CONTENT_TO_SITE:
            articles.filter(sites__id__exact=settings.SITE_ID)
        return articles


class PublishedArticlesManager(ArticlesManager):
    """
    Builds on articles manager to only return articles
    - That are published
    - With a pub_date greater than or equal to now.
    - Belong to a live, active destination assignment.

    Usage is article.published.all()
    """
    def get_queryset(self):
        articles = super(PublishedArticlesManager, self).get_queryset()
        now = datetime.datetime.now()
        articles.filter(destination__active=True, publication='Published', created__lte=now)
        return articles
