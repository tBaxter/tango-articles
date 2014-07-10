
from django.conf.urls import patterns, url
from django.views.generic import ListView

from articles.models import Destination


urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=ListView.as_view(
            queryset=Destination.objects.all(),
            template_name='articles/index.html'
        ),
        name="article_index"
    )
)
