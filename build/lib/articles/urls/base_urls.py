
from django.urls import include, path
from django.views.generic import ListView

from articles.models import Destination


urlpatterns = [
    path('', ListView, {
            'queryset': Destination.objects.all(),
            'template_name': 'articles/index.html'
        },
        name="article_index"
    ),
]
