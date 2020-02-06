# Created by adlh on 2012-10-24
#
# Templates are needed in order render the navigations:
#
# <template_folder>/multinavigation/breadcrumbs.html
# <template_folder>/multinavigation/flatnavigation.html
# <template_folder>/multinavigation/subnavigation.html
# <template_folder>/multinavigation/tabnavigation.html

from django import template
from django.template import RequestContext
from collections import namedtuple
from django.urls import reverse, resolve, Resolver404
from django.urls import NoReverseMatch
import logging

logger = logging.getLogger(__name__)
register = template.Library()

DEBUG_CATCH_NEXT = False

""" A tree node represents each item on a tree-navigation """
TNode = namedtuple('TNode', 'url label active children context')
def build_tnode(n, children, url, active):
    """ Takes a multinavigation.conf.Node namedtuple and builds a tree node. """
    return TNode(url, n.label, active, children, n.context)


@register.inclusion_tag('multinavigation/tabnavigation.html',
        takes_context=True)
def tabnavigation(context, request, nodes):
    """ Returns nodes for the complete navigation tree. """
    url_match = get_url_match(request)
    if not url_match or not url_match.url_name:
        return RequestContext(request, {'nodes': [], 'context': context})
    parents = [n for n in nodes if not n.parent]
    tree_nodes = add_nodes(parents, nodes, request, url_match)
    context['nodes'] = tree_nodes
    return RequestContext(request, {'nodes': tree_nodes, 'context': context})


@register.inclusion_tag('multinavigation/flatnavigation.html',
        takes_context=True)
def flatnavigation(context, request, nodes):
    """ Returns nodes only for the root level. This can be used in combination
    with the subnavigation. """
    tree_nodes = []
    url_match = get_url_match(request)
    if not url_match or not url_match.url_name:
        return RequestContext(request, {'nodes': [], 'context': context})
    for n in nodes:
        if not n.parent:
            url = reverse_url(n, url_match)
            tree_nodes.append(build_tnode(n, [], url, is_active(request, url)))
    return RequestContext(request, {'nodes': tree_nodes, 'context': context})


@register.inclusion_tag('multinavigation/subnavigation.html',
        takes_context=True)
def subnavigation(context, request, nodes):
    """ Returns only a submenu (tree), if any, for the current parent. """
    url_match = get_url_match(request)
    if not url_match or not url_match.url_name:
        return RequestContext(request, {'nodes': [], 'context': context})

    # Find an active parent
    parents = [n for n in nodes if not n.parent]
    tree_nodes = add_nodes(parents, nodes, request, url_match)
    active_parent = [n for n in tree_nodes if n.active]
    if not active_parent:
        return RequestContext(request, {'nodes': [], 'context': context})

    children = active_parent[0].children
    return RequestContext(request, {'nodes': children, 'context': context})


@register.inclusion_tag('multinavigation/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, request, nodes):
    """ Returns the bredcrumbs nodes """
    url_match = get_url_match(request)
    if not url_match or not url_match.url_name:
        return RequestContext(request, {'nodes': [], 'context': context})
    # Find an active parent
    parents = [n for n in nodes if not n.parent]
    tree_nodes = add_nodes(parents, nodes, request, url_match)
    active_parent = [n for n in tree_nodes if n.active]
    if not active_parent:
        return RequestContext(request, {'nodes': [], 'context': context})
    active_parent = active_parent[0]

    # To build the breadcrumbs, we walk all the tree following the active node
    def get_breadcrumbs(node):
        if node.active:
            yield node
        for n in node.children:
            yield from get_breadcrumbs(n)

    b_nodes = [it for it in get_breadcrumbs(active_parent)]

    return RequestContext(request, {'nodes': b_nodes, 'context': context})


def get_root(n, nodes, url_match):
    """ returns the top-most parent in nodes for the given node """
    parent = find_parent(n, nodes, url_match)
    if not parent:
        return n
    if not parent.parent:
        return parent
    else:
        return get_root(parent, nodes, url_match)


def find_parent(child, nodes, url_match):
    if not child.parent:
        return None
    url_name, kwargs = parse_url_name_args(child.parent)
    for node in nodes:
        if match_node(url_name, kwargs, node, url_match):
            return node
    return None


def get_url_match(request):
    """ Get the name of the matching urlpattern """
    if not hasattr(request, 'path'):
        return ""
    # first get the name of the matching urlpattern
    try:
        return resolve(request.path)
    except Resolver404:
        return None


# TODO: make it work with only node context or url|<kwargs>, or a combination
#   of both, without having to repeat same kwargs on url|<kwargs> and {'url_kwargs'...}
def match_node(url_name, kwargs, node, url_match):
    """ Returns true if a node matches url_name and kwargs (if any given) """
    if node.url_name != url_name:
        return False

    DEBUG_CATCH_NEXT = False
    if (len(kwargs) == 2 and kwargs['category'] == 'monkeys' and kwargs['name'] == 'bobo'
            and node.label == 'Dog'):
        DEBUG_CATCH_NEXT = True
    # Check if the kwargs set on the node match the ones from the request
    if DEBUG_CATCH_NEXT:
        test = 123
    nkwargs = get_url_kwargs(node.context.get('url_kwargs', ''), url_match)
    if not kwargs and not nkwargs:
        return True

    return match_subset_kwargs(kwargs, nkwargs)


def match_subset_kwargs(subset_kwargs, kwargs):
    """ Check that all key-value pairs in subset_kwargs match on kwargs """
    # Use sets to easily compare both dicts
    if DEBUG_CATCH_NEXT:
        test = 1234
    s1 = set(kwargs.items())
    s2 = set(subset_kwargs.items())
    is_subset = s2.issubset(s1)
    return is_subset


def parse_url_name_args(string):
    """
    Parse and return url_name and kwargs as a tuple from the node's
    url_name parameter (which can be just the url_name or additionally define
    some kwargs)

    Example: node['url_name'] = 'url_name|kwarg1:value,kwarg2:value'

    """
    chunks = string.split('|')
    url_name = chunks[0]
    kwargs = {}
    if len(chunks) > 1:
        for pair in chunks[1].split(','):
            k, v = pair.strip().split(':')
            k = k.strip()
            v = v.strip()
            if k and v:
                kwargs[k] = v
    return (url_name, kwargs)


def get_children(parent, nodes, url_match):
    children = []
    for c in nodes:
        if c.parent:
            url_name, kwargs = parse_url_name_args(c.parent)
            if match_node(url_name, kwargs, parent, url_match):
                children.append(c)
    return children


def add_nodes(parents, nodes, request, url_match):
    tn_list = []
    for n in parents:
        # children nodes can specify a parent by url_name and additionally
        # with kwargs like this: 'the_url_name|kwd_1:val1,kwd_2:val2'
        children = get_children(n, nodes, url_match)
        tn_children = []
        if children:
            tn_children = add_nodes(children, nodes, request, url_match)
        url = reverse_url(n, url_match)
        active = is_active(request, url)
        # Only add the node if it also has a valid URL, else it wouldn't make
        # sense to add it in the menu
        if url:
            tn_list.append(build_tnode(n, tn_children, url, active))
    return tn_list


def get_url_kwargs(url_kwargs_str, url_match):
    """
    Any needed url parameters can be defined through these ways:

    1. Through the url_kwargs passed with the node's context.

       Example: {'url_kwargs': 'slug:some_category'}

    2. Through the url path of the request. This is the case, when the
       url should be built depending on the current url. Example:
       We've got an url archive/<year>/ and subsets for news, articles, etc.
       Like this: archive/<year>/news, archive/<year>/articles ... And we
       want <year> to be set depending the current url.
       For this to work, the keyword should be present BUT empty on the
       node's context.

       Example: {'url_kwargs': 'year:'}

    """
    # url_kwargs_str should be a str in form 'kwd_1:val_1, kwd_2:val_2, ...'...
    if not url_kwargs_str:
        return {}

    url_kwargs_str = str(url_kwargs_str) # just make sure it's a string

    kwargs = {}
    # put all autocompleted kwargs here
    autocompleted = {}
    for pair in url_kwargs_str.split(','):
        k, v = pair.strip().split(':')
        k = k.strip()
        v = v.strip()
        if k:
            if v:
                kwargs[k] = v
            else:
                # if the value is empty, try to get it from the current URL's
                # path
                if url_match:
                    v = url_match.kwargs.get(k, None)
                    if v:
                        autocompleted[k] = v
    # all kwargs completed from the URL should only be applied,
    # if the others match
    if autocompleted and match_subset_kwargs(kwargs, url_match.kwargs):
        kwargs.update(autocompleted)

    return kwargs


def reverse_url(n, url_match):
    # Get any passed kwargs from the node's context
    kwargs_dict = get_url_kwargs(n.context.get('url_kwargs', ''), url_match)

    try:
        url = reverse(n.url_name, kwargs=kwargs_dict)
    except NoReverseMatch:
        url = ''
    return url


def is_active(request, link_url):
    """ check if the corresponding parts of the given link and the request.path
    match (active).
    For example, if request.path is '/bla/bli/blu/' and link_url is '/bla/',
    '/bla/bli' or /bla/bli/blu/', then is_active should return True
    """
    if not hasattr(request, 'path'):
        return False
    link_parts = link_url.strip('/').split('/')
    request_parts = (request.path).strip('/').split('/')
    if len(request_parts) < len(link_parts):
        return False
    link_comp = '/'.join(link_parts)
    req_comp = '/'.join(request_parts[0:len(link_parts)])
    return link_comp == req_comp


