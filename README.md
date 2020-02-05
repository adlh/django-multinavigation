django-multinavigation
======================

**Goal**: A simple, flexible and DRY way to define and create navigations
(tabnavigation and breadcrumbs).


Quick start
-----------

1) Add app to settings.py:
    ```python
    # setting.py
    INSTALLED_APPS = (
        ...
        'multinavigation',
    )
    ```

2) Be sure all urlpatterns to be used on the navigation are named-patterns, 
because the name will be used as a key for the nodes. Also, for the 
correct `active` status for children and all their parents, the urls 
must be nested. 

    Example: `/animals/`, `/animals/dogs/`, `/animals/dogs/<some_name>`

3) Define your nodes in a context processor.

    A Node is defined like this:

    ```python
    Node = namedtuple('Node', 'url_name label parent context')
    """ Represents a node or item in a navigation
    url_name    -- (string) The name of a named-urlpattern
    label       -- (string) The label to be used in the item
    parent      -- (string) the url_name of its parent or ''. Extra kwargs to be
                    met on the parent may be defined through: 
                    'url_name|kw1:val1,kw2:val2'
    context     -- (dict, optional) Contains extra context for the items, to be
                    used on the templates (if needed) for customization purposes.
    """
    ```
    Example:

    ```python
    # urls.py
    urlpatterns = [
        url(r'^home/$', 'home_view', name='home'),
        url(r'^company/$', 'company_view', name='company'),
        url(r'^media/$', 'company_media', name='media'),
        url(r'^media/news$', 'company_news', name='news'),
        url(r'^media/videos$', 'company_videos', name='videos'),
        url(r'^contact/$', 'contact_view', name='contact'),
   ]
   
   
    # context_processors.py
    from multinavigation.conf import Node

    def multinavigation(request):
        return {
            'MULTINAV_NODES': [
                Node('home', _('Home'), '', {}),
                Node('company', _('Company'), '', {}),
                Node('media', _('Media'), '', {}),
                Node('news', _('News'), 'media', {}),
                Node('videos', _('Videos'), 'media', {}),
                Node('contact', _('Contact'), '', {}),
                ]
            }
    ```

    If there are routes using named parameters, then you can specify the expected kwargs 
    from the request in the node's context ({'url_kwargs': ...}). 

    Also, if using kwargs on nodes with children, then the children can specify their parent url
    with url parameters which must be matched on the parent by the format:
    `parent_url|kwarg1:value,kwarg2:value`
    
    Example:

    ```python
    # urls.py
    urlpatterns = [
        url(r'^home/$', 'home_view', name='home'),
        url(r'^animals/$', 'animals_view', name='animals'),
        url(r'^animals/(?P<category>[a-z]+)/$', 'animals_category_view', name='animals_category'),
        url(r'^animals/(?P<category>[a-z]+)/(?P<name>[a-z]+)/$', 'pet_view', name='pet'),
        url(r'^contact/$', 'contact_view', name='contact'),
    ]
   
    # context_processors.py
    from multinavigation.conf import Node

    def multinavigation(request):
        return {
            'MULTINAV_NODES': [
                Node('home', 'Home', '', {}),
                Node('animals', 'Animals', '', {}),
                # define the kwargs expected on the request in the node's context: 
                # {'url_kwargs': 'kwarg1:val1,kwarg2:val2...'}
                Node('animals_category', 'Dogs', 'animals', {'url_kwargs': 'category:dogs'}),
                Node('animals_category', 'Cats', 'animals', {'url_kwargs': 'category:cats'}),
                Node('animals_category', 'Birds', 'animals', {'url_kwargs': 'category:birds'}),
                Node('animals_category', 'Monkeys', 'animals', {'url_kwargs': 'category:monkeys'}),
                Node('contact', 'Contact', '', {}),
                # when refering to a parent with kwargs, define them after the url_name:
                # '<url_name>|kwarg1:val1,kwarg2:val2...'
                Node('pet', 'Dog', 'animals_category|category:dogs', {'url_kwargs': 'category:dogs,name:'}),
                # ... also, when dealing with kwargs that are dynamically set and have no dedicated route 
                # (like here the route 'pets' for 'Cat', 'Bird', etc.) you can leave the value empty 
                # (e.g. 'name:') and it will be defined through the request kwargs, if present.
                Node('pet', 'Cat', 'animals_category|category:cats', {'url_kwargs': 'category:cats,name:'}),
                Node('pet', 'Bird', 'animals_category|category:birds', {'url_kwargs': 'category:birds,name:'}),
                Node('pet', 'Monkey', 'animals_category|category:monkeys', {'url_kwargs': 'category:monkeys,name:'}),
            ]
       }
    ```

4) Add your context_processor in settings.py, e.g.

    NOTE: Be sure you have `django.core.context_processors.request` included in
    your `TEMPLATE_CONTEXT_PROCESSORS` as well. This will add a `request` context
    varialble in your templates, which you must pass as the first parameter to the
    multinavigation template tags.

    Add the following lines to add the processors to the defaults in settings.py:

    ```python
    # settings.py

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
