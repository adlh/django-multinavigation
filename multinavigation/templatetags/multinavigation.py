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
    parents = [n for n in nodes if not n.parent]
    tree_nodes = add_nodes(parents, nodes, request)
    context['nodes'] = tree_nodes
    return RequestContext(request, {'nodes': tree_nodes,})


@register.inclusion_tag('multinavigation/flatnavigation.html',
        takes_context=True)
def flatnavigation(context, request, nodes):
    """ Returns nodes only for the root level. This can be used in combination
    with the subnavigation. """
    tree_nodes = []
    for n in nodes:
        url = reverse(n.url_name)
        if not n.parent:
            tree_nodes.append(build_tnode(n, [], url, is_active(request, url)))
    return RequestContext(request, {'nodes': tree_nodes,})


@register.inclusion_tag('multinavigation/subnavigation.html',
        takes_context=True)
def subnavigation(context, request, nodes):
    """ Returns only a submenu (tree), if any, for the current parent. """
    urlname = get_urlname(request)
    if not urlname:
        return []
    subnodes = []
    children = []
    for n in nodes:
        if n.url_name == urlname:
            # this is the active node, get top-most parent first
            parent = get_root(n, nodes)
            children = [c for c in nodes if c.parent == parent.url_name]
    tree_nodes = add_nodes(children, nodes, request)
    return RequestContext(request, {'nodes': tree_nodes,})


@register.inclusion_tag('multinavigation/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, request, nodes):
    """ Returns the bredcrumbs nodes """
    urlname = get_urlname(request)
    if not urlname:
        return []
    b_nodes = []
    # if any breadcrumbs are found the first one is the active one
    find_breadcrumbs(urlname, nodes, b_nodes, True)
    # now reverse to get parent > child > grandchild > ...
    b_nodes.reverse()
    return RequestContext(request, {'nodes': b_nodes,})


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


def get_urlname(request):
    """ Get the name of the matching urlpattern """
    if not hasattr(request, 'path'):
        return ""
    # first get the name of the matching urlpattern
    try:
        return resolve(request.path).url_name
    except Resolver404:
        return ""


def find_breadcrumbs(url_name, nodes, b_nodes, active):
    for n in nodes:
        if n.url_name == url_name:
            url = reverse(n.url_name)
            b_nodes.append(build_tnode(n, [], url, active))
            if n.parent:
                find_breadcrumbs(n.parent, nodes, b_nodes, False)


def add_nodes(parents, nodes, request):
    tn_list = []
    for n in parents:
        children = [c for c in nodes if c.parent == n.url_name]
        tn_children = add_nodes(children, nodes, request)
        url = reverse(n.url_name)
        active = is_active(request, url)
        tn_list.append(build_tnode(n, tn_children, url, active))
    return tn_list


def is_active(request, link_url):
    """ check if the corresponding parts of the given link and the request.path
    match (active) """
    if not hasattr(request, 'path'):
        return False
    # get the last or relevant "level" of this link and compare it with
    # corresponding part on request-url
    link_parts = link_url.strip('/').split('/')
    request_parts = (request.path).strip('/').split('/')
    if len(request_parts) < len(link_parts):
        return False
    return link_parts[-1] == request_parts[len(link_parts)-1]

