# -*- encoding: utf-8 -*-
from rest_framework.routers import DefaultRouter
from Empresas.api.views import EmpresaViewSet, EmpleadoViewSet, ProcesoViewSet, PerfilViewSet, CategoriaProcesoViewSet, \
    TareasViewSet

__author__ = 'linglung'
from django.conf.urls import patterns, url, include

router = DefaultRouter()
router.register(r'empresa', EmpresaViewSet)
router.register(r'empleado', EmpleadoViewSet)
router.register(r'proceso', ProcesoViewSet)
router.register(r'perfil', PerfilViewSet)
router.register(r'categoria', CategoriaProcesoViewSet)
router.register(r'tarea', TareasViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    )