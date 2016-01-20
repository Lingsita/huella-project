__author__ = 'linglung'
from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from Formularios.models import Formulario, Campo


class FormularioSerializer(ModelSerializer):
    class Meta:
        model = Formulario
        fields = ('pk', 'nombre', 'descripcion',  'active')
        depth = 1

class CampoSerializer(ModelSerializer):
    class Meta:
        model = Campo
        fields = ('pk', 'id_campo', 'nombre', 'descripcion', 'tipo', 'min', 'max', 'formulario',  'active')
        depth = 1


