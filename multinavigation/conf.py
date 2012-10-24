from collections import namedtuple

Node = namedtuple('Node', 'url_name label parent context')
""" 
Represents a node or item in a navigation
url_name: a string matching the name of a named-urlpattern
label: the label to be used in the item
parent: the url_name of its parent or ''
context: a dictionary containing extra context for the items (e.g. css-class)

"""


