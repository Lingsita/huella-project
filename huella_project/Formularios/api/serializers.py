__author__ = 'linglung'
from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from Formularios.models import Formulario


class FormularioSerializer(ModelSerializer):
    class Meta:
        model = Formulario

        fields = ('pk','nombre', 'url', 'active')
