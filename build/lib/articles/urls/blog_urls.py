from django.urls import include, path
from django.views.generic import TemplateView, ListView

from articles.models import Destination
from articles.views import ArticleDetail, ArticleList, EditBlogEntry, CreateBlogEntry, add_image

urlpatterns = [
    path(
        'entry/thank-you/',
        TemplateView,
        {'template_name': 'blogs/thank-you.html'},
        name='add_entry_thanks',
    ),
    path('<slug:destination_slug>/add-entry/', CreateBlogEntry, name="blog_add_entry"),
    path(
        route='<slug:destination_slug>/<slug:entry_slug>/add-images/',
        view=add_image,
        name="blog_add_image",
    ),
    path('<slug:blog_slug>/edit-entry/<int:pk>/', EditBlogEntry, name="blog_edit_entry"),
    path('',
        ListView, 
        {'queryset': Destination.blogs.all(), 'template_name': 'blogs/blog_list.html'},
        name="blog_list"
    ),
    path('<slug:destination_slug>', ArticleList, name="blog_detail"),
    path('<slug:destination_slug>/<slug:slug>/', ArticleDetail, name="blog_entry_detail"),
]
