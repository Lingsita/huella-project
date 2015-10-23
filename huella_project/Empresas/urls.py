__author__ = 'linglung'
from django.conf.urls import patterns, url

urlpatterns = patterns('Empresas.views',
    url(r'^list$', 'empresas_list'),
    url(r'^empresas$', 'admin_empresas', name='admin_empresas'),
    url(r'^detail/(?P<pk>[0-9]+)/$', 'empresa_detail'),
    )