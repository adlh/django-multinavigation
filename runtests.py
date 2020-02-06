#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.test_app.test_settings'

def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['src.multinavigation', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
