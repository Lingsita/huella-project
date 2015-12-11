from django.views.generic.base import TemplateView

__author__ = 'linglung'
from django.conf.urls import patterns, url

urlpatterns = patterns('Empresas.views',
    url(r'^list$', 'empresas_list'),
    url(r'^empresas$', 'admin_empresas', name='admin_empresas'),
    url(r'^detail/$', 'empresa_detail', name="detail"),
    url(r'^rest$', 'empresas_rest'),
    url(r'^detail/empleados.html$', TemplateView.as_view(template_name="empresa/empleados.html")),
    url(r'^detail/procesos.html$', TemplateView.as_view(template_name="empresa/procesos.html")),
    url(r'^detail/perfiles.html$', TemplateView.as_view(template_name="empresa/perfiles.html")),
    url(r'^detail/tareas.html$', TemplateView.as_view(template_name="empresa/tareas.html")),
    )