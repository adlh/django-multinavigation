django-multinavigation
======================

Goal: A simple, flexible and DRY way to define and create navigations
(tabnavigation and breadcrumbs).

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

If there are any url's which need named parameters, then you should pass them
with the node's context under the keyword 'url_kwargs', so that the url can be
reversed correctly. 

NOTE: the given value of the parameter in the node, will ALWAYS be overriden
in the case, the request-url defines the parameter itself. Or in other words,
if the request.path is /bla/my-slug-2/2020/ ... then slug will be 'my-slug-2'
and year will be 2020, not matter, which defaults were given in url_kwargs. 
But it is important to define this parameters on the node's context, or else
the resolve of the url will fail.

An example would be:

```python
# urls.py
...
url(r'^bla/(?P<slug>[-\w]+)/(?P<year>[0-9]{4})/$', 'bla', name='bla_params')
...

# context_processors.py
from multinavigation.conf import Node

def multinavigation(request):
    bla_dict = {'url_kwargs':'year:{}, slug:{}'.format(2012, 'my-slug')}
    return {
        'MULTINAV_NODES': [
            Node('home', _('Home'), '', {}),
            Node('company', _('Company'), '', {}),
            Node('contact', _('Contact'), '', {}),
            Node('bla_params', _('Bla'), '', bla_dict),
            ]
        }
```



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

4) Add your context_processor in settings.py, e.g.
```python
# settings.py

TEMPLATE_CONTEXT_PROCESSORS += (
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
