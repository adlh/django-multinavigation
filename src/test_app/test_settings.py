DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'src.multinavigation',
     'src.test_app'
)

MIDDLEWARE = (
     'django.contrib.sessions.middleware.SessionMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
     'django.contrib.auth.middleware.AuthenticationMiddleware',
     'django.contrib.messages.middleware.MessageMiddleware',
     'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'src.test_app.context_processors.multinavigation'
            ],
        },
    },
]

# Load models directly to pick up test-only models
# See: http://stackoverflow.com/a/25267435/347942
MIGRATION_MODULES = {'src.multinavigation': None}

SECRET_KEY = 'this-is-just-for-tests-so-not-that-secret'

ROOT_URLCONF = 'src.test_app.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}
