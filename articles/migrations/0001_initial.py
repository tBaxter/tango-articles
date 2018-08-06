# Generated by Django 2.0.7 on 2018-08-02 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import tango_shared.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
        #('photos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overline', models.CharField(blank=True, help_text='A short headline over the main headline.', max_length=200, null=True, verbose_name='Kicker/Overline')),
                ('title', models.CharField(help_text='The title for this content.', max_length=200, verbose_name='Title/Headline')),
                ('subhead', models.CharField(blank=True, help_text='A short extra headline below the main headline.', max_length=200, verbose_name='Subhead/Deck')),
                ('slug', models.SlugField(help_text='Used for URLs and identification.\n        Will auto-fill, but can be edited with caution.\n        ', max_length=200)),
                ('summary', models.TextField(blank=True, help_text="You should summarize the content.\n        It's better for search engines, and for people browsing lists of content.\n        If you don't, a summary will be created. But you should.\n        ", verbose_name='Summary description')),
                ('summary_formatted', models.TextField(blank=True, editable=False, help_text='Stores HTML formatted, sanitized version of summary')),
                ('featured', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('enable_comments', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('has_image', models.BooleanField(default=False, editable=False, max_length=200)),
                ('guest_author', models.CharField(blank=True, help_text='If the author is not on staff, enter their name.', max_length=200)),
                ('body', models.TextField()),
                ('body_formatted', models.TextField(blank=True, editable=False)),
                ('pull_quote', models.TextField(blank=True)),
                ('endnote', models.TextField(blank=True, help_text='A short note after the body.', null=True)),
                ('override_url', models.URLField(blank=True, help_text='If this story is actaully published elsewhere, give the URL.')),
                ('publication', models.CharField(choices=[('Draft', 'Draft'), ('Proofed', 'Proofed'), ('Published', 'Published')], default='Published', max_length=32, verbose_name='Publication status')),
                ('author', models.ForeignKey(blank=True, help_text='If the author is on-staff, select their name.', limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='Size should be a minimum of 720px and no more than 2000px high or wide.', upload_to=tango_shared.models.set_img_path)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('byline', models.CharField(blank=True, max_length=200, null=True)),
                ('credit', models.CharField(blank=True, max_length=200, null=True, verbose_name='Credit/source')),
                ('order', models.IntegerField(blank=True, help_text='For manual sorting.', null=True)),
                ('thumb', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('is_vertical', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'abstract': False,
                'ordering': ['order', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, help_text='The visible name of the attachment', max_length=200)),
                ('attachment', models.FileField(upload_to='attachments/articles/')),
                ('filetype', models.CharField(editable=False, max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Brief',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Limit yourself to 140 characters for Twitter integration')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, help_text='Use full URL, with http://', max_length=200, null=True)),
                ('tweet', models.BooleanField(default=False, verbose_name='Send to Twitter')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('summary', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='img/content/cats')),
                ('is_for_blog', models.BooleanField(default=False, help_text='Limit this category to blogs.')),
            ],
            options={
                'verbose_name_plural': 'sub-categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('icon', models.ImageField(blank=True, help_text='If this is not a personal blog, provide a representative image', upload_to='img/content/icons/')),
                ('active', models.BooleanField(default=True)),
                ('is_blog', models.BooleanField(default=True)),
                ('author', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Blogger', 'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'destination',
                'verbose_name_plural': 'destinations',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='LinkRoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(help_text='Only needed if this is not a sidebar')),
                ('text', models.TextField()),
                ('text_formatted', models.TextField(blank=True, editable=False, null=True)),
                ('is_sidebar', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=tango_shared.models.set_img_path)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_sidebars', to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='Size should be a minimum of 720px and no more than 2000px high or wide.', upload_to=tango_shared.models.set_img_path)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('byline', models.CharField(blank=True, max_length=200, null=True)),
                ('credit', models.CharField(blank=True, max_length=200, null=True, verbose_name='Credit/source')),
                ('order', models.IntegerField(blank=True, help_text='For manual sorting.', null=True)),
                ('thumb', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('is_vertical', models.BooleanField(default=False, editable=False)),
                ('sidebar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='articles.Sidebar')),
            ],
            options={
                'abstract': False,
                'ordering': ['order', '-id'],
            },
        ),
        migrations.AddField(
            model_name='link',
            name='linkroll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.LinkRoll'),
        ),
        migrations.AddField(
            model_name='article',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='articles.Destination'),
        ),
        migrations.AddField(
            model_name='article',
            name='galleries',
            field=models.ManyToManyField(blank=True, related_name='article_galleries', to='photos.Gallery'),
        ),
        migrations.AddField(
            model_name='article',
            name='sections',
            field=models.ManyToManyField(blank=True, to='articles.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='sites',
            field=models.ManyToManyField(default=[1], to='sites.Site'),
        ),
        migrations.AddField(
            model_name='article',
            name='articles',
            field=models.ManyToManyField(
                blank=True, 
                limit_choices_to={'publication': 'Published'}, 
                related_name='_article_articles_+', 
                to='articles.Article'
            )
        ),
        migrations.AddField(
            model_name='articleImage',
            name='article',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, 
                to='articles.Article'
            )
        ),
        migrations.AddField(
            model_name='attachment',
            name='article',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, 
                to='articles.Article'
            )
        ),
    ]
