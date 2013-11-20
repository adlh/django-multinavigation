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
from django.core.urlresolvers import reverse, resolve, Resolver404
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
        url = reverse_url(n, url_match)
        if not n.parent:
            tree_nodes.append(build_tnode(n, [], url, is_active(request, url)))
    return RequestContext(request, {'nodes': tree_nodes, 'context': context})


@register.inclusion_tag('multinavigation/subnavigation.html',
        takes_context=True)
def subnavigation(context, request, nodes):
    """ Returns only a submenu (tree), if any, for the current parent. """
    url_match = get_url_match(request)
    urlname = url_match.url_name if url_match else ''
    if not urlname:
        return []
    subnodes = []
    children = []
    for n in nodes:
        if n.url_name == urlname:
            # this is the active node, get top-most parent first
            parent = get_root(n, nodes)
            children = [c for c in nodes if c.parent == parent.url_name]
    tree_nodes = add_nodes(children, nodes, request, url_match)
    return RequestContext(request, {'nodes': tree_nodes, 'context': context})


@register.inclusion_tag('multinavigation/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, request, nodes):
    """ Returns the bredcrumbs nodes """
    url_match = get_url_match(request)
    urlname = url_match.url_name if url_match else ''
    if not urlname:
        return []
    b_nodes = []
    # if any breadcrumbs are found the first one is the active one
    find_breadcrumbs(urlname, nodes, b_nodes, True, url_match)
    # now reverse to get parent > child > grandchild > ...
    b_nodes.reverse()
    return RequestContext(request, {'nodes': b_nodes, 'context': context })


def get_root(n, nodes):
    """ returns the top-most parent in nodes for the given node """
    if not n.parent:
        return n
    for node in nodes:
        if n.parent == node.url_name:
            if not node.parent:
                return node
            else:
                return get_root(node, nodes)


def get_url_match(request):
    """ Get the name of the matching urlpattern """
    if not hasattr(request, 'path'):
        return ""
    # first get the name of the matching urlpattern
    try:
        return resolve(request.path)
    except Resolver404:
        return None


def find_breadcrumbs(url_name, nodes, b_nodes, active, url_match):
    for n in nodes:
        if n.url_name == url_name:
            url = reverse_url(n, url_match)
            b_nodes.append(build_tnode(n, [], url, active))
            if n.parent:
                find_breadcrumbs(n.parent, nodes, b_nodes, False, url_match)


def add_nodes(parents, nodes, request, url_match):
    tn_list = []
    for n in parents:
        children = [c for c in nodes if c.parent == n.url_name]
        tn_children = add_nodes(children, nodes, request, url_match)
        url = reverse_url(n, url_match)
        active = is_active(request, url)
        tn_list.append(build_tnode(n, tn_children, url, active))
    return tn_list


def get_url_kwargs(url_kwargs_str):
    # url_kwargs should be a str in form 'kwd_1:val_1, kwd_2:val_2, ...'...
    url_kwargs_str = str(url_kwargs_str) # just make sure it's a string
    url_kwargs = {}
    if url_kwargs_str:
        for pair in url_kwargs_str.split(','):
            k, v = pair.strip().split(':')
            k = k.strip()
            v = v.strip()
        if k and v:
            url_kwargs[k] = v
    return url_kwargs


def reverse_url(n, url_match):
    url_kwargs = n.context.get('url_kwargs', '')
    kwargs_dict = {}
    if url_kwargs:
        kwargs_dict = get_url_kwargs(url_kwargs)
    # if there is a required kwarg defined in the node-context but it's empty
    # and it's in the url_match present, update dict
    if url_match:
        for k in kwargs_dict.keys():
            v = url_match.kwargs.get(k, None)
            if v:
                kwargs_dict[k] = v
    url = reverse(n.url_name, kwargs=kwargs_dict)
    return url


def is_active(request, link_url):
    """ check if the corresponding parts of the given link and the request.path
    match (active).
    For example, if requeest.path is '/bla/bli/blu/' and link_url is '/bla/',
    '/bla/bli' or /bla/bli/blu/' is_active should return True
    """
    if not hasattr(request, 'path'):
        return False
    link_parts = link_url.strip('/').split('/')
    request_parts = (request.path).strip('/').split('/')
    if len(request_parts) < len(link_parts):
        return False
    return '/'.join(link_parts) == '/'.join(request_parts[0:len(link_parts)])


