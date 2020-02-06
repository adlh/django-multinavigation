from src.multinavigation.conf import Node

def multinavigation(request):
    return {
        'MULTINAV_NODES': [
            Node('home', 'Home', '', {}),
            Node('animals', 'Animals', '', {}),
            Node('animals_category', 'Dogs', 'animals', {'url_kwargs': 'category:dogs'}),
            Node('animals_category', 'Cats', 'animals', {'url_kwargs': 'category:cats'}),
            Node('animals_category', 'Birds', 'animals', {'url_kwargs': 'category:birds'}),
            Node('animals_category', 'Monkeys', 'animals', {'url_kwargs': 'category:monkeys'}),
            Node('contact', 'Contact', '', {}),
            # Node('pet', 'Dog', 'animals_category|category:dogs', {'url_kwargs': 'category:dogs,name:'}),
            # Node('pet', 'Cat', 'animals_category|category:cats', {'url_kwargs': 'category:cats,name:'}),
            # Node('pet', 'Bird', 'animals_category|category:birds', {'url_kwargs': 'category:birds,name:'}),
            # Node('pet', 'Monkey', 'animals_category|category:monkeys', {'url_kwargs': 'category:monkeys,name:'}),
        ],
        'DEEP_NESTED_MULTINAV_NODES': [
            Node('url-a', 'A', '', {}),
            Node('url-aa', 'AA', 'url-a', {}),
            Node('url-ab', 'AB', 'url-a', {}),
            Node('url-aba', 'ABA', 'url-ab', {}),
            Node('url-abb', 'ABB', 'url-ab', {}),
            Node('url-abc', 'ABC', 'url-ab', {}),
            Node('url-abca', 'ABCA', 'url-abc', {}),
            Node('url-abcb', 'ABCB', 'url-abc', {}),
            Node('url-abcc', 'ABCC', 'url-abc', {}),
            Node('url-abcd', 'ABCD', 'url-abc', {}),
            Node('url-b', 'B', '', {}),
            Node('url-c', 'C', '', {}),
            Node('url-ca', 'CA', 'url-c', {}),
            Node('url-cb', 'CB', 'url-c', {}),
            Node('url-cc', 'CC', 'url-c', {}),
        ]
    }
