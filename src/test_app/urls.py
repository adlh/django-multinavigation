from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^home/$', TemplateView.as_view(template_name='page.html'), name='home'),
    url(r'^animals/$', TemplateView.as_view(template_name='page.html'), name='animals'),
    url(r'^animals/(?P<category>[a-z]+)/$', TemplateView.as_view(template_name='page.html'), name='animals_category'),
    url(r'^animals/(?P<category>[a-z]+)/(?P<name>[a-z]+)/$', TemplateView.as_view(template_name='page.html'), name='pet'),
    url(r'^contact/$', TemplateView.as_view(template_name='page.html'), name='contact'),
]
