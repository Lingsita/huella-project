from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from Empresas.api.filters import EmpresaFilter
from Empresas.api.pagination import StandardResultsSetPagination
from Empresas.forms import CrearEmpresaForm
from Empresas.models import Empresa
from Empresas.serializers import EmpresaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EmpresaFilter

    # def list(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset.filter(active=True)
        return queryset



    # def get(self, request, format=None):

# class EmpresasRest(APIView):
#     serializer= EmpresaSerializer
#     def get(self, request, format=None):
#         empresas = Empresa.objects.filter(active=True)
#         resp= self.serializer(empresas, many=True)
#         return Response(resp.data)
#     def post(self, request, format=None):
#         empresa= self.serializer(data= request.data)
#         if empresa.is_valid():
#             empresa.save()
#             resp= self.serializer(empresa.data, many=False)
#             #return Response(resp.data)
#             return JSONResponse(empresa.data)
#         else:
#
#             return Response({'message': 'this is my message for fail post'})
#
# empresas_rest= EmpresasRest.as_view()

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def admin_empresas(request):
    if request.method == "POST":
        form = CrearEmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save()
            return redirect('admin_empresas')
    else:
        print('dasdasm,n,mn,')
        form = CrearEmpresaForm()
        print(form)
    return render(request, 'admin_empresas.html', {'form': form})


def empresas_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    print('dasdas')
    if request.method == 'GET':
        empresas = Empresa.objects.filter(active=True)
        serializer = EmpresaSerializer(empresas, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmpresaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def empresa_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        empresa = Empresa.objects.get(pk=pk)
    except Empresa.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EmpresaSerializer(empresa)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EmpresaSerializer(empresa, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        empresa.delete()
        return HttpResponse(status=204)

