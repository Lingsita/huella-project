from rest_framework.routers import DefaultRouter
from Empresas.api.views import EmpresaViewSet

__author__ = 'linglung'
from django.conf.urls import patterns, url, include

router = DefaultRouter()
router.register(r'empresa', EmpresaViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    )