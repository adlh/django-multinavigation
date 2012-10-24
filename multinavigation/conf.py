from collections import namedtuple

Node = namedtuple('Node', 'url_name label parent context')
"""
Usage:
    navtree = [
     Node(url_name='url1', label='URL 1', parent='', context={ 
         'markup1': '<i class="icon-bla"></i>', 'class2': 'bla'}),
     Node(url_name='url2', label='URL 2', parent='', context={}),
     Node(url_name='url2.1', label='URL 2.1', parent='url2', context={}),
     Node(url_name='url3', label='URL 3', parent='', context={})]
"""
