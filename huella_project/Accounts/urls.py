__author__ = 'linglung'

from django.conf.urls import patterns, url

urlpatterns = patterns('Accounts.views',
    url(r'^logout$','logout_session', name ='logout'),
    url(r'^documentos$','docs_empleado', name ='docs_empleado'),
    )