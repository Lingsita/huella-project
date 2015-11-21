from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from Formularios.api.filters import FormularioFilter
from Formularios.api.pagination import StandardResultsSetPagination
from Formularios.api.serializers import FormularioSerializer
from Formularios.models import Formulario


class FormularioViewSet(viewsets.ModelViewSet):
    serializer_class = FormularioSerializer
    queryset = Formulario.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = FormularioFilter

    def list(self, request):
        queryset = Formulario.objects.filter(active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # def get_queryset(self):
    #     queryset = self.queryset.filter(active=True)
    #     return queryset

