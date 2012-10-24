django-multinavigation
======================

Goal: A simple, flexible and DRY way to define and create navigations (tabnavigation and breadcrumbs).

INSTALLATION:

1) add app to settings.py:
```python
# setting.py
INSTALLED_APPS = (
    ...
    'multinavigation',
)
```

2) Be sure all urlpatterns to be used on the navigation are named-patterns, 
because the name will be used as a key for the nodes.

3) define your nodes in a context processor, e.g.:

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

4) Add your context_processor in settings.py, e.g.
```python
# settings.py

TEMPLATE_CONTEXT_PROCESSORS += (
    'mysite.context_processors.multinavigation',
)
```

5) Define your template(s)
...

6) Ready to use the templatetag
...
