# -*- encoding: utf-8 -*-
__author__ = 'linglung'
from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from Empresas.models import Empresa, Empleado, Proceso, Perfil, Tarea, CategoriaProceso, Formato, Documento


class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('pk','nombre', 'direccion', 'NIT', 'email','telefono1','telefono2', 'active')


class EmpleadoSerializer(ModelSerializer):
    class Meta:
        model = Empleado
        fields = ('pk','usuario', 'nombre', 'apellido', 'identificacion','tipo_documento','perfil','direccion', 'codigo', 'telefono1', 'telefono2', 'is_admin', 'foto', 'active')
        depth = 2

class CategoriaProcesoSerializer(ModelSerializer):
    class Meta:
        model = CategoriaProceso
        fields = ('pk','nombre', 'descripcion','active')

        depth = 1

class ProcesoSerializer(ModelSerializer):
    class Meta:
        model = Proceso
        fields = ('pk','nombre', 'codigo', 'categoria', 'descripcion', 'formatos_asignados', 'active')
        depth = 1

class PerfilSerializer(ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('pk','nombre', 'codigo','descripcion' ,'empresa', 'procesos', 'formatos_asignados', 'active')
        depth = 1

class TareasSerializer(ModelSerializer):
    class Meta:
        model = Tarea
        fields = ('pk','nombre', 'empleado', 'descripcion', 'fecha_inicio', 'fecha_fin', 'active')
        depth = 1

class FormatosSerializer(ModelSerializer):
    class Meta:
        model = Formato
        fields = ('pk', 'nombre', 'formulario', 'descripcion', 'empresa', 'active')
        depth = 1

class DocumentoSerializer(ModelSerializer):
    class Meta:
        model = Documento
        fields = ('pk', 'codigo','formato', 'formato_default', 'elaboro', 'proceso', 'tipo_documento', 'fecha_emision', 'paginas', 'external_link', 'is_external', 'archivo', 'restringido', 'ubicacion_original', 'active', 'version')
        depth = 1

