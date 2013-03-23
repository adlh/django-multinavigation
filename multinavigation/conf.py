from collections import namedtuple

Node = namedtuple('Node', 'url_name label parent context')
""" Represents a node or item in a navigation
url_name    -- (string) The name of a named-urlpattern
label       -- (string) The label to be used in the item
parent      -- (string) the url_name of its parent or ''
context     -- (dict, optional) Contains extra context for the items, to be
                used on the templates (if needed) for customization purposes.
"""

