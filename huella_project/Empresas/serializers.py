__author__ = 'linglung'
from django.forms import widgets
from rest_framework import serializers
from Empresas.models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('pk','nombre', 'direccion', 'NIT', 'active')
