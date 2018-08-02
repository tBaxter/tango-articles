from django.urls import path
from django.views.generic import DetailView

from articles.views import article_detail, article_list

urlpatterns = [
    path('<slug:slug>/', article_detail, name="article_detail"),
    path('', article_list, name="article_list"),
    path('briefs/<int:id>/', DetailView, name="brief_detail"),
]
