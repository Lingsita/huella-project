from django.views.generic.base import TemplateView

__author__ = 'linglung'
from django.conf.urls import patterns, url

urlpatterns = patterns('Empresas.views',
    url(r'^list$', 'empresas_list'),
    url(r'^empresas$', 'admin_empresas', name='admin_empresas'),
    url(r'^detail/(?P<id>\d+)$', 'empresa_detail', name="detail"),
    url(r'^inicio$', 'admin_empresa_detail', name="empresa_detail"),
    url(r'^rest$', 'empresas_rest'),
    url(r'^documento/nuevo/(?:(?P<id>\d+))?$', 'nuevo_documento', name='nuevo_documento'),
    url(r'^documento/nuevo/formato/(?:(?P<proceso>\d+)?)(?:(\/)?(?P<id>\d+)?)$', 'nuevo_documento_by_formato', name='nuevo_documento_by_formato'),
    url(r'^detail/empleados.html$', TemplateView.as_view(template_name="empresa/empleados.html")),
    url(r'^detail/procesos.html$', TemplateView.as_view(template_name="empresa/procesos.html")),
    url(r'^detail/perfiles.html$', TemplateView.as_view(template_name="empresa/perfiles.html")),
    url(r'^detail/tareas.html$', TemplateView.as_view(template_name="empresa/tareas.html")),
    url(r'^documento.html$', TemplateView.as_view(template_name="empleado/documento.html")),
    url(r'^empleados.html$', TemplateView.as_view(template_name="empresa/empleados.html")),
    url(r'^procesos.html$', TemplateView.as_view(template_name="empresa/procesos.html")),
    url(r'^perfiles.html$', TemplateView.as_view(template_name="empresa/perfiles.html")),
    url(r'^tareas.html$', TemplateView.as_view(template_name="empresa/tareas.html")),

    )