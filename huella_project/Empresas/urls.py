__author__ = 'linglung'
from django.conf.urls import patterns, url

urlpatterns = patterns('Empresas.views',
    url(r'^list$', 'empresas_list'),
    url(r'^empresas$', 'admin_empresas', name='admin_empresas'),
    url(r'^detail', 'empresa_detail', name="detail"),
    url(r'^rest$', 'empresas_rest')
    )