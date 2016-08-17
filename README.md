django-multinavigation
======================

Goal: A simple, flexible and DRY way to define and create navigations
(tabnavigation and breadcrumbs).

INSTALLATION:

1) Add app to settings.py:
```python
# setting.py
INSTALLED_APPS = (
    ...
    'multinavigation',
)
```


2) Be sure all urlpatterns to be used on the navigation are named-patterns, 
because the name will be used as a key for the nodes.

3) Define your nodes in a context processor.

A Node is defined like this:

```python
Node = namedtuple('Node', 'url_name label parent context')
""" Represents a node or item in a navigation
url_name    -- (string) The name of a named-urlpattern
label       -- (string) The label to be used in the item
parent      -- (string) the url_name of its parent or ''
context     -- (dict, optional) Contains extra context for the items, to be
                used on the templates (if needed) for customization purposes.
"""
```
Example:

```python
# context_processors.py
from multinavigation.conf import Node

def multinavigation(request):
    return {
        'MULTINAV_NODES': [
            Node('home', _('Home'), '', {}),
            Node('company', _('Company'), '', {}),
            Node('contact', _('Contact'), '', {}),
            Node('disclaimer', _('Disclaimer'), '', {}),
            ]
        }
```

If there are any url's which need named parameters, then there are 2 ways to
pass them through.

1. Through the node's context under the keyword 'url_kwargs'. 

    For example:

    ```python
    ...
        Node('category', _('Category'), '', {'url_kwargs': 'slug:some_category'}),
    ...
    ```

2. Or through the request's path, to be able to build URLs dinamically
   depending on which path is set. Example: Let's say we have an archive with
   news and pics as subnav items. Now depending if we're on */archive/2014/* we
   want the subnav items set to */archive/2014/news/* and */archive/2014/pics/*
   respectively.

    Example:

    ```python
    # urls.py
    ...
        url(r'^archive/(?P<year>[0-9]{4})/$', 'archive', name='archive_year'),
        url(r'^archive/(?P<year>[0-9]{4})/news$', 'archive_news', name='archive_news'),
        url(r'^archive/(?P<year>[0-9]{4})/pics$', 'archive_pics', name='archive_pics'),
    ...

    # context_processors.py
    from multinavigation.conf import Node

    # We define the nodes in the subnav like this:

    def multinavigation(request):
    #...
        Node('archive_news', _('News'), 'archive', {'url_kwargs': 'year:'}),
        Node('archive_pics', _('Pictures'), 'archive', {'url_kwargs': 'year:'}),
    #...
    ```

4) Add your context_processor in settings.py, e.g.

NOTE: Be sure you have `django.core.context_processors.request` included in
your `TEMPLATE_CONTEXT_PROCESSORS` as well. This will add a `request` context
varialble in your templates, which you must pass as the first parameter to the
multinavigation template tags.

Add the following lines to add the processors to the defaults in settings.py:

```python
j settings.py

import django.conf.global_settings as DEFAULT_SETTINGS

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'mysite.context_processors.multinavigation',
)
```


5) Define your template(s), you can also just use or customize the
example-templates provided.

6) Ready to use the templatetags. Some examples could be:
```html
<div class="navbar">
    <ul class="nav nav-pills">
        {% tabnavigation request MULTINAV_NODES %}
    </ul>
</div>

<ul class="breadcrumb">
    {% breadcrumbs request MULTINAV_NODES %}
</ul>
```
