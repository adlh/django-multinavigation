from django.test import TestCase
from pprint import pformat
import logging

logger = logging.getLogger(__name__)

class MultinavigationTemplateTagTests(TestCase):
    def test_active_root_without_children(self):
        response = self.client.get('/home/')
        logger.warn('****\n/home/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('home', url_match.url_name)

        # flatnavigation
        self.assertContains(
            response,
            '''<flatnavigation>
- [Home] [/home/] [active] []
- [Animals] [/animals/] [] []
- [Contact] [/contact/] [] []
</flatnavigation>''',
            status_code=200,
            html=True
        )

        # subnavigation
        self.assertContains(
            response,
            '<subnavigation></subnavigation>',
            status_code=200,
            html=True
        )

        # breadcrumbs
        self.assertContains(
            response,
            '''<breadcrumbs>Home [/home/] > </breadcrumbs>''',
            status_code=200,
            html=True
        )

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
- [Home] [/home/] [active] []
- Animals [+]
<dropdown>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</dropdown>
- [Contact] [/contact/] [] []
</tabnavigation>''',
            status_code=200,
            html=True
        )

    def test_active_node_with_children(self):
        response = self.client.get('/animals/')
        logger.warn('****\n/animals/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('animals', url_match.url_name)

        # flatnavigation
        self.assertContains(
            response,
            '''<flatnavigation>
- [Home] [/home/] [] []
- [Animals] [/animals/] [active] []
- [Contact] [/contact/] [] []
</flatnavigation>''',
            status_code=200,
            html=True
        )

        # subnavigation
        self.assertContains(
            response,
            '''<subnavigation>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</subnavigation>''',
            status_code=200,
            html=True
        )

        # breadcrumbs
        self.assertContains(
            response,
            '''<breadcrumbs>Animals [/animals/] > </breadcrumbs>''',
            status_code=200,
            html=True
        )

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
- [Home] [/home/] [] []
- Animals [+] [active]
<dropdown>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</dropdown>
- [Contact] [/contact/] [] []
</tabnavigation>''',
            status_code=200,
            html=True
        )

    def test_active_child(self):
        response = self.client.get('/animals/cats/')
        logger.warn('****\n/animals/cats/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('animals_category', url_match.url_name)

        # flatnavigation
        self.assertContains(
            response,
            '''<flatnavigation>
- [Home] [/home/] [] []
- [Animals] [/animals/] [active] []
- [Contact] [/contact/] [] []
</flatnavigation>''',
            status_code=200,
            html=True
        )

        # subnavigation
        self.assertContains(
            response,
            '''<subnavigation>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [active] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</subnavigation>''',
            status_code=200,
            html=True
        )

        # breadcrumbs
        self.assertContains(
            response,
            '''<breadcrumbs>Animals [/animals/] > Cats [/animals/cats/] > </breadcrumbs>''',
            status_code=200,
            html=True
        )

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
- [Home] [/home/] [] []
- Animals [+] [active]
<dropdown>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [active] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</dropdown>
- [Contact] [/contact/] [] []
</tabnavigation>''',
            status_code=200,
            html=True
        )

    def test_3rd_level_node(self):
        response = self.client.get('/animals/cats/fiffy/')
        logger.warn('****\n/animals/cats/fiffy/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('pet', url_match.url_name)

        # flatnavigation
        self.assertContains(
            response,
            '''<flatnavigation>
- [Home] [/home/] [] []
- [Animals] [/animals/] [active] []
- [Contact] [/contact/] [] []
</flatnavigation>''',
            status_code=200,
            html=True
        )

        # subnavigation
        self.assertContains(
            response,
            '''<subnavigation>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [active] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</subnavigation>''',
            status_code=200,
            html=True
        )

        # breadcrumbs
        self.assertContains(
            response,
            '''<breadcrumbs>Animals [/animals/] > Cats [/animals/cats/] > Cat [/animals/cats/fiffy/] > 
            </breadcrumbs>''',
            status_code=200,
            html=True
        )

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
- [Home] [/home/] [] []
- Animals [+] [active]
<dropdown>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [active] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [] []
</dropdown>
- [Contact] [/contact/] [] []
</tabnavigation>''',
            status_code=200,
            html=True
        )

    def test_3rd_level_node_2(self):
        response = self.client.get('/animals/monkeys/bobo/')
        logger.warn('****\n/animals/monkeys/bobo/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('pet', url_match.url_name)

        # flatnavigation
        self.assertContains(
            response,
            '''<flatnavigation>
- [Home] [/home/] [] []
- [Animals] [/animals/] [active] []
- [Contact] [/contact/] [] []
</flatnavigation>''',
            status_code=200,
            html=True
        )

        # subnavigation
        self.assertContains(
            response,
            '''<subnavigation>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [active] []
</subnavigation>''',
            status_code=200,
            html=True
        )

        # breadcrumbs
        self.assertContains(
            response,
            '''<breadcrumbs>Animals [/animals/] > Monkeys [/animals/monkeys/] > Monkey [/animals/monkeys/bobo/] > 
            </breadcrumbs>''',
            status_code=200,
            html=True
        )

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
- [Home] [/home/] [] []
- Animals [+] [active]
<dropdown>
- [Dogs] [/animals/dogs/] [] []
- [Cats] [/animals/cats/] [] []
- [Birds] [/animals/birds/] [] []
- [Monkeys] [/animals/monkeys/] [active] []
</dropdown>
- [Contact] [/contact/] [] []
</tabnavigation>''',
            status_code=200,
            html=True
        )
