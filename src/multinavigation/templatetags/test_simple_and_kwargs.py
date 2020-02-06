from django.test import TestCase
import logging

logger = logging.getLogger(__name__)

OUTPUT_DEBUG = True

class MultinavigationTemplateTagTests(TestCase):
    def test_active_root_without_children(self):
        response = self.client.get('/home/')
        if OUTPUT_DEBUG:
            logger.debug('****\n/home/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('home', url_match.url_name)

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
            - [Home] [/home/] [active] []
            - Animals [+]
            [tab]
                - [Dogs] [/animals/dogs/] [] []
                - [Cats] [/animals/cats/] [] []
                - [Birds] [/animals/birds/] [] []
                - [Monkeys] [/animals/monkeys/] [] []
            - [Contact] [/contact/] [] []
            </tabnavigation>''',
            status_code=200,
            html=True
        )

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

    def test_active_node_with_children(self):
        response = self.client.get('/animals/')
        if OUTPUT_DEBUG:
            logger.debug('****\n/animals/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('animals', url_match.url_name)

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
            - [Home] [/home/] [] []
            - Animals [+] [active]
            [tab]
                - [Dogs] [/animals/dogs/] [] []
                - [Cats] [/animals/cats/] [] []
                - [Birds] [/animals/birds/] [] []
                - [Monkeys] [/animals/monkeys/] [] []
            - [Contact] [/contact/] [] []
            </tabnavigation>''',
            status_code=200,
            html=True
        )

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

    def test_active_child(self):
        response = self.client.get('/animals/cats/')
        if OUTPUT_DEBUG:
            logger.debug('****\n/animals/cats/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('animals_category', url_match.url_name)

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
            - [Home] [/home/] [] []
            - Animals [+] [active]
            [tab]
                - [Dogs] [/animals/dogs/] [] []
                - [Cats] [/animals/cats/] [active] []
                - [Birds] [/animals/birds/] [] []
                - [Monkeys] [/animals/monkeys/] [] []
            - [Contact] [/contact/] [] []
            </tabnavigation>''',
            status_code=200,
            html=True
        )

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

    def test_3rd_level_node(self):
        response = self.client.get('/animals/monkeys/bobo/')
        if OUTPUT_DEBUG:
            logger.debug('****\n/animals/monkeys/bobo/\n***\n{}'.format(str(response.content)))
        url_match = response.resolver_match
        self.assertEqual('pet', url_match.url_name)

        # tabnavigation
        self.assertContains(
            response,
            '''<tabnavigation>
            - [Home] [/home/] [] []
            - Animals [+] [active]
            [tab]
                - [Dogs] [/animals/dogs/] [] []
                - [Cats] [/animals/cats/] [] []
                - [Birds] [/animals/birds/] [] []
                - [Monkeys] [/animals/monkeys/] [active] []
            - [Contact] [/contact/] [] []
            </tabnavigation>''',
            status_code=200,
            html=True
        )

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
            '''<breadcrumbs>Animals [/animals/] > Monkeys [/animals/monkeys/] > </breadcrumbs>''',
            status_code=200,
            html=True
        )

