from django.test import TestCase
import logging

logger = logging.getLogger(__name__)


class MultinavigationTemplateTagDeepNestedTests(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get('/a/b/c/d/')
        self.url_match = self.response.resolver_match

    def test_route(self):
        self.assertEqual('url-abcd', self.url_match.url_name)

    def test_tabnavigation_at_4th_level_active_item(self):
        self.assertContains(
            self.response,
            '''<tabnavigation>
            - A [+] [active]
            [tab]
                - [AA] [/a/a/] [] []
                - AB [+] [active]
                [tab]
                    - [ABA] [/a/b/a/] [] []
                    - [ABB] [/a/b/b/] [] []
                    - ABC [+] [active]
                    [tab]
                        - [ABCA] [/a/b/c/a/] [] []
                        - [ABCB] [/a/b/c/b/] [] []
                        - [ABCC] [/a/b/c/c/] [] []
                        - [ABCD] [/a/b/c/d/] [active] []
            - [B] [/b/] [] []
            - C [+]
            [tab]
                - [CA] [/c/a/] [] []
                - [CB] [/c/b/] [] []
                - [CC] [/c/c/] [] []
            </tabnavigation>''',
            status_code=200,
            html=True
        )

    def test_flatnavigation_at_4th_level_active_item(self):
        self.assertContains(
            self.response,
            '''<flatnavigation>
            - [A] [/a/] [active] []
            - [B] [/b/] [] []
            - [C] [/c/] [] []
            </flatnavigation>''',
            status_code=200,
            html=True
        )

    def test_subnavigation_at_4th_level_active_item(self):
        self.assertContains(
            self.response,
            '''<subnavigation>
            - [AA] [/a/a/] [] []
            - [AB] [/a/b/] [active] []
            </subnavigation>''',
            status_code=200,
            html=True
        )

    def test_breadcrumbs_at_4th_level_active_item(self):
        self.assertContains(
            self.response,
            '''<breadcrumbs> A [/a/] > AB [/a/b/] > ABC [/a/b/c/] > ABCD [/a/b/c/d/] > </breadcrumbs>''',
            status_code=200,
            html=True
        )

