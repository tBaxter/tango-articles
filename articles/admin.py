from django.contrib import admin

from .forms import BaseArticleForm
from .models import ArticleImage, Sidebar, Destination, Category, Brief, Article
from .models import supports_video, supports_polls, supports_galleries

from tango_admin.admin import TextCounterWidget

if supports_video:
    from video.admin import VideoInline


class ArticleImagesInline(admin.TabularInline):
    model = ArticleImage
    extra = 3


class SidebarInline(admin.TabularInline):
    model = Sidebar
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    form = BaseArticleForm

    class Media:
        js = (
            '/static/admin/js/jquery-ui-1.10.3.custom-sortable.min.js',
            '/static/admin/js/inline_reorder.js',
        )

    ordering = ['-created']
    list_display = ('title', 'author', 'destination', 'created',)
    list_filter = ('created', 'last_modified', 'enable_comments', 'publication', 'destination')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['body', 'title']
    filter_horizontal = ['sections', 'articles']
    inlines = [
        ArticleImagesInline,
        SidebarInline,
    ]
    related = ('Related', {
        'fields': ['articles'],
        'description': 'Other content directly related to this article'
    })
    if supports_video:
        inlines.append(VideoInline)
    if supports_galleries:
        related[1]['fields'].insert(0, 'galleries')
        filter_horizontal.append('galleries')
    if supports_polls:
        related[1]['fields'].insert(0, 'polls')

    fieldsets = (
        ('Author info', {'fields': (('author', 'guest_author'))}),
        ('Header', {'fields': ('overline', 'title', 'subhead')}),
        ('Content', {'fields': ('summary', 'body', 'pull_quote', 'endnote')}),
        ('Admin fields', {
            'description': 'You should rarely, if ever, need to touch these fields.',
            'fields': ('slug', 'enable_comments', 'sites', 'override_url'),
            'classes': ['collapse']
        }),
        ('Routing', {'fields': ('destination', 'sections')}),
        related,
        ('Meta',     {
            'fields': (('publication'), 'featured'),
            'description': 'Additional information about this story'
        }),
        ('Bulk photo upload', {
            'fields': ('upload',),
            'description': "Upload multiple photos at once, if you don't want to handle them individually."
        })
    )

    def save_model(self, request, obj, form, change):
        #return HttpResponse(request.FILES.getlist('upload'))
        obj.save()
        for img in request.FILES.getlist('upload'):
            ArticleImage(
                image = img,
                article = obj
            ).save()
        obj.bulk_upload = None
        obj.save()


class BriefAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'text')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            kwargs['widget'] = TextCounterWidget()
        return super(BriefAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Destination)
admin.site.register(Category)
admin.site.register(Brief, BriefAdmin)
admin.site.register(Article, ArticleAdmin)
