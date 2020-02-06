from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^home/$', TemplateView.as_view(template_name='page.html'), name='home'),
    url(r'^animals/$', TemplateView.as_view(template_name='page.html'), name='animals'),
    url(r'^animals/(?P<category>[a-z]+)/$', TemplateView.as_view(template_name='page.html'), name='animals_category'),
    url(r'^animals/(?P<category>[a-z]+)/(?P<name>[a-z]+)/$', TemplateView.as_view(template_name='page.html'), name='pet'),
    url(r'^contact/$', TemplateView.as_view(template_name='page.html'), name='contact'),
]

urlpatterns += [
    url(r'^a/$', TemplateView.as_view(template_name='nested.html'), name='url-a'),
    url(r'^a/a/$', TemplateView.as_view(template_name='nested.html'), name='url-aa'),
    url(r'^a/b/$', TemplateView.as_view(template_name='nested.html'), name='url-ab'),
    url(r'^a/b/a/$', TemplateView.as_view(template_name='nested.html'), name='url-aba'),
    url(r'^a/b/b/$', TemplateView.as_view(template_name='nested.html'), name='url-abb'),
    url(r'^a/b/c/$', TemplateView.as_view(template_name='nested.html'), name='url-abc'),
    url(r'^a/b/c/a/$', TemplateView.as_view(template_name='nested.html'), name='url-abca'),
    url(r'^a/b/c/b/$', TemplateView.as_view(template_name='nested.html'), name='url-abcb'),
    url(r'^a/b/c/c/$', TemplateView.as_view(template_name='nested.html'), name='url-abcc'),
    url(r'^a/b/c/d/$', TemplateView.as_view(template_name='nested.html'), name='url-abcd'),
    url(r'^b/$', TemplateView.as_view(template_name='nested.html'), name='url-b'),
    url(r'^c/$', TemplateView.as_view(template_name='nested.html'), name='url-c'),
    url(r'^c/a/$', TemplateView.as_view(template_name='nested.html'), name='url-ca'),
    url(r'^c/b/$', TemplateView.as_view(template_name='nested.html'), name='url-cb'),
    url(r'^c/c/$', TemplateView.as_view(template_name='nested.html'), name='url-cc'),
]
