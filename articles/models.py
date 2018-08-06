from itertools import chain

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from .managers import DestinationManager, BlogManager, ArticlesManager, PublishedArticlesManager
from .signals import auto_tweet

from tango_shared.models import ContentImage, BaseContentModel, BaseSidebarContentModel
from tango_shared.utils.sanetize import sanetize_text

########## CONFIG ###########

supports_video = 'video' in settings.INSTALLED_APPS
supports_polls = 'polls' in settings.INSTALLED_APPS
supports_galleries = 'photos' in settings.INSTALLED_APPS
supports_autotagging = 'autotagger' in settings.INSTALLED_APPS

if supports_autotagging:
    from autotagger.autotag_content import autotag

# Comment moderation settings
closing = getattr(settings, 'COMMENTS_CLOSE_AFTER', 30)
moderating = getattr(settings, 'COMMENTS_MOD_AFTER', 30)

PUBLICATION_CHOICES = (
    ('Draft', 'Draft'),
    ('Proofed', 'Proofed'),
    ('Published', 'Published'),
)

# News site settings.
NEWS_SOURCE = getattr(settings, 'NEWS_SOURCE', False)

########## END CONFIG ###########


class Destination(models.Model):
    """
    Defines destinations content may be assigned to
    and allows for routing to the correct destination.

    Destinations are the top-level assignments.
    This is where you would create a blog, an article groups, etc.

    To-do: add site(s)
    """
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True, 'groups__name': 'Blogger'},
        blank=True,
        null=True
    )
    icon = models.ImageField(
        upload_to="img/content/icons/",
        blank=True,
        help_text="If this is not a personal blog, provide a representative image"
    )
    active = models.BooleanField(default=True)
    is_blog = models.BooleanField(default=True)

    objects = DestinationManager()
    blogs = BlogManager()

    class Meta:
        verbose_name = "destination"
        verbose_name_plural = "destinations"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_blog:
            return '/blogs/' + self.slug
        return '/' + self.slug

    def get_feed_url(self):
        return '/feeds' + self.get_absolute_url()


class Category(models.Model):
    """
    Allows for content categorization.
    Categories can be used by one or more destination.
    They can also be limited to only blogs.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    summary = models.TextField(blank=True)
    image = models.ImageField(upload_to="img/content/cats", blank=True)
    is_for_blog = models.BooleanField(default=False, help_text="Limit this category to blogs.")

    class Meta:
        verbose_name_plural = "sub-categories"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Article(BaseContentModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_staff': True},
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="""If the author is on-staff, select their name."""
    )
    guest_author = models.CharField(
        max_length=200,
        blank=True,
        help_text="""If the author is not on staff, enter their name."""
    )
    body = models.TextField()
    body_formatted = models.TextField(blank=True, editable=False)
    pull_quote = models.TextField(blank=True)
    endnote = models.TextField(
        blank=True,
        null=True,
        help_text="A short note after the body."
    )
    override_url = models.URLField(
        blank=True,
        help_text="If this story is actaully published elsewhere, give the URL."
    )
    publication = models.CharField(
        "Publication status",
        max_length=32,
        choices=PUBLICATION_CHOICES,
        default='Published'
    )

    # RELATIONSHIPS
    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT
    )
    sections = models.ManyToManyField(Category, blank=True)
    articles = models.ManyToManyField(
        'self',
        related_name="related_articles",
        blank=True,
        limit_choices_to={'publication': 'Published'}
    )

    if supports_video:
        videos = GenericRelation('video.Video')
    if supports_polls:
        polls = models.ManyToManyField('polls.Poll', blank=True)
    if supports_galleries:
        galleries = models.ManyToManyField(
            'photos.Gallery',
            related_name="article_galleries",
            blank=True
        )

    if NEWS_SOURCE:
        opinion = models.BooleanField("Opinion/Editorial", default=False)
        source = models.CharField(
            max_length=200,
            default=NEWS_SOURCE,
            blank=True,
            null=True
        )
        dateline = models.CharField(max_length=200, blank=True, null=True)

    # Managers
    objects = ArticlesManager()
    published = PublishedArticlesManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        If override_url was given, use that.
        Otherwise, if the content belongs to a blog, use a blog url.
        If not, use a regular article url.
        """
        if self.override_url:
            return self.override_url
        if self.destination.is_blog:
            return reverse('blog_entry_detail', args=[self.destination.slug, self.slug])
        return reverse('article_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Store summary if none was given
        and created formatted version of body text.
        """
        if not self.summary:
            self.summary = truncatewords(self.body, 50)
        self.body_formatted = sanetize_text(self.body)
        super(Article, self).save()

    def get_top_assets(self):
        """
        Returns chained list of top assets (photos and video) for commonized templates.
        """
        imgs = self.articleimage_set.all()
        try:
            vids = self.videos.all()
        except AttributeError:
            # handles case where videos are not in installed apps
            # or otherwise unavailable
            vids = []
        return list(chain(imgs, vids))

    def get_image(self):
        try:
            return self.articleimage_set.all()[0]
        except IndexError:
            return None

    def autotag_body(self):
        """
        Auto-inserts links for matching content and establishes M2M relationships.
        See utils.autotag_content import autotag for details.
        """
        if supports_autotagging:
            return autotag(self, self.body_formatted)
        return self.body

    def get_comment_count(self):
        from django.contrib.contenttypes.models import ContentType
        from tango_comments.models import Comment
        ctype = ContentType.objects.get(name__exact='article')
        num_comments = Comment.objects.filter(content_type=ctype.id, object_pk=self.id).count()
        return num_comments


class Sidebar(BaseSidebarContentModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="related_sidebars"
    )


class Attachment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )
    filename = models.CharField(
        max_length=200,
        blank=True,
        help_text="The visible name of the attachment"
    )
    attachment = models.FileField(upload_to='attachments/articles/')
    filetype = models.CharField(max_length=4, editable=False)

    def save(self):
        self.filetype = self.attachment.name.split(".")[-1]
        super(Attachment, self).save()


class Brief(models.Model):
    text = models.TextField(help_text="Limit yourself to 140 characters for Twitter integration")
    pub_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Use full URL, with http://"
    )
    sites = models.ManyToManyField(Site)
    tweet = models.BooleanField("Send to Twitter", default=False)

    def __str__(self):
        return str(self.pub_date)

    def get_absolute_url(self):
        return reverse('brief_detail', args=[self.id])


class ArticleImage(ContentImage):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )


class SidebarImage(ContentImage):
    sidebar = models.ForeignKey(
        Sidebar,
        on_delete=models.CASCADE
    )


class LinkRoll(models.Model):
    """
    Defines a list of external links
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Link(models.Model):
    """
    An individual link for a LinkRoll.
    """
    display_text = models.CharField(max_length=200)
    url = models.URLField()
    linkroll = models.ForeignKey(
        LinkRoll,
        on_delete=models.CASCADE
    )

models.signals.post_save.connect(auto_tweet, sender=Brief)
