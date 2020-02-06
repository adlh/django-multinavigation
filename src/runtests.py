#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.test_app.test_settings'
import src.test_app.test_settings

# if not settings.configured:
#     settings.configure(
#         DATABASES={
#             'default': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': ':memory:',
#             }
#         },
#         INSTALLED_APPS=(
#             'django.contrib.auth',
#             'django.contrib.contenttypes',
#             'django.contrib.sessions',
#             'multinavigation',
#             'test_app'
#         ),
#         MIDDLEWARE=(
#             'django.contrib.sessions.middleware.SessionMiddleware',
#             'django.middleware.common.CommonMiddleware',
#             'django.middleware.csrf.CsrfViewMiddleware',
#             'django.contrib.auth.middleware.AuthenticationMiddleware',
#             'django.contrib.messages.middleware.MessageMiddleware',
#             'django.middleware.clickjacking.XFrameOptionsMiddleware',
#         ),
#         TEMPLATES=[
#             {
#                 'BACKEND': 'django.template.backends.django.DjangoTemplates',
#                 'DIRS': [],
#                 'APP_DIRS': True,
#                 'OPTIONS': {
#                     'context_processors': [
#                         'django.template.context_processors.debug',
#                         'django.contrib.messages.context_processors.messages',
#                         'django.template.context_processors.request',
#                         'test_app.context_processors.multinavigation'
#                     ],
#                 },
#             },
#         ],
#         # Load models directly to pick up test-only models
#         # See: http://stackoverflow.com/a/25267435/347942
#         MIGRATION_MODULES={'multinavigatoin': None},
#         SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
#         ROOT_URLCONF='test_app.urls',
#     )


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['multinavigation', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
