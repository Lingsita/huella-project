__author__ = 'linglung'
import django_filters
from Formularios.models import Formulario
from Empresas.serializers import EmpresaSerializer
from rest_framework import filters
from rest_framework import generics

class FormularioFilter(django_filters.FilterSet):

    nombre = django_filters.CharFilter(name="nombre", lookup_type='icontains')

    class Meta:
        model = Formulario
        fields = ['nombre']