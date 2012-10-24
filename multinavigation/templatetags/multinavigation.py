# Created by adlh on 2012-10-24
#
# Templates are needed in order render the navigations:
#
# <template_folder>/multinavigation/tabnavigation.html
# <template_folder>/multinavigation/breadcrumbs.html

from django.conf import settings
from django import template
from collections import namedtuple
from django.core.urlresolvers import reverse, resolve
import logging

logger = logging.getLogger(__name__)
register = template.Library()

""" A tree node represents each item on a tree-navigation """
TNode = namedtuple('Node', 'url label active children context')

@register.inclusion_tag('multinavigation/tabnavigation.html')
def tabnavigation(request, nodes):
    # build the tree for the navigation
    parents = [n for n in nodes if not n.parent]
    tree_nodes = add_nodes(parents, nodes, request)
    return {'nodes': tree_nodes,}

@register.inclusion_tag('multinavigation/breadcrumbs.html')
def breadcrumbs(request, nodes):
    if not hasattr(request, 'path'):
        return []
    # first get the name of the matching urlpattern 
    urlname = resolve(request.path).url_name
    b_nodes = []
    # if any breadcrumbs are found the first one is the active one
    find_breadcrumbs(urlname, nodes, b_nodes, True)
    # now reverse to get parent > child > grandchild > ...
    b_nodes.reverse()
    return {'nodes': b_nodes,}

def find_breadcrumbs(url_name, nodes, b_nodes, active):
    for n in nodes:
        if n.url_name == url_name:
            b_nodes.append(TNode(reverse(n.url_name), n.label, active, [], n.context))
            if n.parent:
                find_breadcrumbs(n.parent, nodes, b_nodes, False)


def add_nodes(parents, nodes, request):
    tn_list = []
    for n in parents:
        children = [c for c in nodes if c.parent == n.url_name]
        tn_children = add_nodes(children, nodes, request)
        url = reverse(n.url_name)
        tn_list.append(TNode(url, n.label, is_active(request, url), tn_children, n.context))
    return tn_list

def is_active(request, link_url):
    """ check if the corresponding parts of the given link and the request.path match (active) """
    if not hasattr(request, 'path'):
        return False
    # get the last or relevant "level" of this link and compare it with corresponding part on request-url
    link_parts = link_url.strip('/').split('/')
    request_parts = (request.path).strip('/').split('/')
    if len(request_parts) < len(link_parts):
        return False 
    return link_parts[-1] == request_parts[len(link_parts)-1] 

