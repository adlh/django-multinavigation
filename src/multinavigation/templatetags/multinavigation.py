# Created by adlh on 2012-10-24
#
# Templates are needed in order render the navigations:
#
# <template_folder>/multinavigation/tabnavigation.html
# <template_folder>/multinavigation/breadcrumbs.html

from django.conf import settings
from django import template
from django.template import RequestContext
from collections import namedtuple
from django.urls import reverse, resolve, Resolver404
from django.urls import NoReverseMatch
from pprint import pformat
import logging

logger = logging.getLogger(__name__)
register = template.Library()

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
    url_name = url_match.url_name if url_match else ''
    kwargs = url_match.kwargs
    if not url_name:
        return []
    subnodes = []
    children = []
    for n in nodes:
        if match_node(url_name, kwargs, n, url_match):
            # this is the active node, get top-most parent first
            parent = get_root(n, nodes, url_match)
            children = get_children(parent, nodes, url_match)
    tree_nodes = add_nodes(children, nodes, request, url_match)
    return RequestContext(request, {'nodes': tree_nodes, 'context': context})


@register.inclusion_tag('multinavigation/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, request, nodes):
    """ Returns the bredcrumbs nodes """
    url_match = get_url_match(request)
    if not url_match or not url_match.url_name:
        return []
    b_nodes = []
    # if any breadcrumbs are found the first one is the active one
    find_breadcrumbs(None, nodes, b_nodes, True, url_match)
    # now reverse to get parent > child > grandchild > ...
    b_nodes.reverse()
    return RequestContext(request, {'nodes': b_nodes, 'context': context })


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


def match_node(url_name, kwargs, node, url_match):
    """ Returns true if a node matches url_name and kwargs (if any given) """
    if node.url_name != url_name:
        return False
    if not kwargs:
        return True
    nkwargs = get_url_kwargs(node.context.get('url_kwargs', ''), url_match)

    return match_subset_kwargs(kwargs, nkwargs)


def find_breadcrumbs(url_name_args, nodes, b_nodes, active, url_match):
    """
    Find a node matching url_name and any kwargs specified by the url_name_args
    or if none given from the url_match (our starting point).
    If a node is found add it to b_nodes and if the node has a parent repeat
    the procedure.

    """
    kwargs = {}
    url_name = ''
    if not url_name_args:
        kwargs = url_match.kwargs
        url_name = url_match.url_name
    else:
        url_name, kwargs = parse_url_name_args(url_name_args)

    found = [n for n in nodes if match_node(url_name, kwargs, n, url_match)]
    if found:
        found = found[0]
    if not found:
        return

    url = reverse_url(found, url_match)
    b_nodes.append(build_tnode(found, [], url, active))

    if found.parent:
        find_breadcrumbs(found.parent, nodes, b_nodes, False, url_match)


def match_subset_kwargs(subset_kwargs, kwargs):
    """ Check that all key-value pairs in subset_kwargs match on kwargs """
    # Use sets to easily compare both dicts
    s1 = set(kwargs.items())
    s2 = set(subset_kwargs.items())
    return s2.issubset(s1)


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
        tn_children = add_nodes(children, nodes, request, url_match)
        url = reverse_url(n, url_match)
        active = is_active(request, url)
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
                        kwargs[k] = v
    return kwargs


def reverse_url(n, url_match):
    # Get any passed kwargs from the node's context
    kwargs_dict = get_url_kwargs(n.context.get('url_kwargs', ''), url_match)

    try:
        url = reverse(n.url_name, kwargs=kwargs_dict)
    except NoReverseMatch:
        url = '#'
    return url


def is_active(request, link_url):
    """ check if the corresponding parts of the given link and the request.path
    match (active).
    For example, if requeest.path is '/bla/bli/blu/' and link_url is '/bla/',
    '/bla/bli' or /bla/bli/blu/', then is_active should return True
    """
    if not hasattr(request, 'path'):
        return False
    link_parts = link_url.strip('/').split('/')
    request_parts = (request.path).strip('/').split('/')
    if len(request_parts) < len(link_parts):
        return False
    return '/'.join(link_parts) == '/'.join(request_parts[0:len(link_parts)])


