from setuptools import setup, find_packages

setup(
    name='django-multinavigation',
    version='1.3',
    description='A Django app to easily generate navigation and breadcrumbs',
    long_description='A simple, flexible and DRY way to define and create navigations (tabnavigation and breadcrumbs) from the urlpatterns and a context-processor.',
    long_description_content_type='text/x-rst',
    url='https://github.com/adlh/django-multinavigation',
    license='MIT',
    author='Andrea de la Huerta',
    author_email='info@metamorfosys.de',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=2.7, >=3.5.*, <4',
    project_urls={
        'Bug Reports': 'https://github.com/adlh/django-multinavigation',
        'Source': 'https://github.com/adlh/django-multinavigation',
    },
    setup_requires=['pytest-runner']
)
