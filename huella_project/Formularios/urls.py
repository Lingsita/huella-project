__author__ = 'linglung'
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('Formularios.views',
    url(r'^$', 'index_formatos', name='index'),
    url(r'^list-formularios$', 'index_formularios', name='index_formularios'),
    url(r'^muestra_form/$', 'montar_formulario_dinamico', name='url_muestra_form'),
    url(r'^muestra_form/(?P<id>\d+)$', 'montar_formulario_dinamico', name='muestra_form'),
    url(r'^nuevo/$', 'nuevo_formato', name='nuevo_form'),
    url(r'^nuevo-formulario$', 'nuevo_formulario', name='nuevo_formulario'),
    url(r'^documento.html$', TemplateView.as_view(template_name="empleado/documento.html")),
    )