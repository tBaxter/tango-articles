SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sessions',

    'tango_shared',
    'articles',
    # installed by shared, keeps templates happy
    'typogrify',
    'easy_thumbnails',
    'voting',
    #'photos'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'articles.urls.article_urls'

SITE_ID = 1

PAGINATE_BY = 20

#stripped down middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
