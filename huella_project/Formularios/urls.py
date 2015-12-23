__author__ = 'linglung'
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('Formularios.views',
    url(r'^$', 'index_formularios', name='index'),
    url(r'^nuevo/$', 'nuevo_formato', name='nuevo_form'),
    url(r'^documento.html$', TemplateView.as_view(template_name="empleado/documento.html")),
    )