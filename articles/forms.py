from django.conf import settings

from django.forms import ModelForm, HiddenInput, FileField, FileInput

from .models import Article, ArticleImage
from .models import NEWS_SOURCE

supports_polls = 'polls' in settings.INSTALLED_APPS
supports_galleries = 'photos' in settings.INSTALLED_APPS


class BaseArticleForm(ModelForm):
    """
    Base form for articles. Supports bulk upload.
    """
    upload = FileField(
        required=False,
        label = "Upload multiple file(s)",
        help_text="""
            You can upload multiple JPG files at once, or individual files below.
        """,
        widget=FileInput(attrs={'multiple': 'multiple'})
    )

    class Meta:
        model = Article
        # to do: append article to fields rather than re-declare
        fields = [
            'author', 'guest_author', 'overline', 'title', 'subhead', 'summary', 'body', 
            'pull_quote', 'endnote', 'override_url', 'slug', 'enable_comments', 'sites',
            'publication', 'destination', 'sections', 'articles', 'upload', 'featured',
        ]
 
        if supports_polls:
            fields.append('polls')
        if supports_galleries:
            fields.append('galleries')
        if NEWS_SOURCE:
            fields.extend(['opinion', 'source', 'dateline'])
        

class BlogEntryForm(BaseArticleForm):  
    """
    Public form for adding and editing blog entries.
    """

    class Meta:
        model = Article
        fields = (
            'title',
            'summary',
            'body',
            'upload'
        )


class BlogEntryImageForm(ModelForm):
    class Meta:
        model = ArticleImage
        fields = ('image', 'caption', 'article', 'byline')
        widgets = {
            'article': HiddenInput(),
            'byline':  HiddenInput()
        }
