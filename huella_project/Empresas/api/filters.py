# -*- encoding: utf-8 -*-
__author__ = 'linglung'
import django_filters
from Empresas.models import Empresa, Empleado, Proceso, Perfil, CategoriaProceso
from Empresas.serializers import EmpresaSerializer
from rest_framework import filters
from rest_framework import generics

class EmpresaFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')
    NIT = django_filters.CharFilter(name="NIT", lookup_type='icontains')
    class Meta:
        model = Empresa
        fields = ['nombre', 'NIT']

class EmpleadoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')
    apellido = django_filters.CharFilter(name="apellido", lookup_type='icontains')
    identificacion = django_filters.CharFilter(name="identificacion", lookup_type='icontains')
    codigo = django_filters.CharFilter(name="codigo", lookup_type='icontains')
    class Meta:
        model = Empleado
        # fields = ['nombre', 'apellido,' 'identificacion', 'codigo']

class ProcesoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')
    categoria = django_filters.CharFilter(name="categoria", lookup_type='icontains')
    descripcion = django_filters.CharFilter(name="descripcion", lookup_type='icontains')

    class Meta:
        model = Proceso
        # fields = ['nombre', 'categoria,' 'descripcion']

class CategoriaProcesoFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')

    class Meta:
        model = CategoriaProceso
        # fields = ['nombre', 'categoria,' 'descripcion']

class PerfilFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')
    codigo = django_filters.CharFilter(name="codigo", lookup_type='icontains')

    class Meta:
        model = Perfil
        # fields = ['nombre', 'apellido,' 'identificacion', 'codigo']