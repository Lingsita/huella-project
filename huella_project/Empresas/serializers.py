__author__ = 'linglung'
from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from Empresas.models import Empresa


class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('pk','nombre', 'direccion', 'NIT', 'email','telefono1','telefono2', 'active')
