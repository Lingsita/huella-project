from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from Empresas.models import Empresa, Empleado, Formato
from Formularios.api.filters import FormularioFilter
from Formularios.api.pagination import StandardResultsSetPagination
from Formularios.api.permissions import IsBusinessAdmin
from Formularios.api.serializers import FormularioSerializer
from Formularios.models import Formulario, Campo


class FormularioViewSet(viewsets.ModelViewSet):
    serializer_class = FormularioSerializer
    queryset = Formulario.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)
    filter_class = FormularioFilter

    def list(self, request):
        queryset = Formulario.objects.filter(active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    @detail_route(methods=['get'])
    def get_forms(self, request, id=None):

        queryset = Formulario.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        formulario=Formulario(nombre=request.data['nombre'], descripcion=request.data['descripcion'])
        formulario.save()
        for c in request.data['campos']:
            campo=Campo(id_campo=c['id_campo'],
                        nombre = c['nombre'],
                        descripcion= c['descripcion'],
                        tipo=c['tipo'],
                        max=c['max'],
                        min=c['min'],
                        formulario= formulario
                        )
            campo.save()

        serializer = FormularioSerializer(formulario)
        return Response(serializer.data)

class FormularioAdminViewSet(viewsets.ModelViewSet):
    serializer_class = FormularioSerializer
    queryset = Formulario.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsBusinessAdmin, )
    filter_class = FormularioFilter

    def list(self, request):
        empleado= Empleado.objects.get(usuario__user=request.user)
        empresa=empleado.perfil.empresa
        queryset=Formato.objects.filter(active=True)
        queryset = Formulario.objects.filter(active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    @detail_route(methods=['get'])
    def get_forms(self, request, id=None):

        queryset = Formulario.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        formulario=Formulario(nombre=request.data['nombre'], descripcion=request.data['descripcion'])
        formulario.save()
        for c in request.data['campos']:
            campo=Campo(id_campo=c['id_campo'],
                        nombre = c['nombre'],
                        descripcion= c['descripcion'],
                        tipo=c['tipo'],
                        max=c['max'],
                        min=c['min'],
                        formulario= formulario
                        )
            campo.save()

        serializer = FormularioSerializer(formulario)
        return Response(serializer.data)