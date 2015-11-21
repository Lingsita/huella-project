__author__ = 'linglung'
import django_filters
from Empresas.models import Empresa
from Empresas.serializers import EmpresaSerializer
from rest_framework import filters
from rest_framework import generics

class EmpresaFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')
    NIT = django_filters.CharFilter(name="NIT", lookup_type='icontains')
    class Meta:
        model = Empresa
        fields = ['nombre', 'NIT']