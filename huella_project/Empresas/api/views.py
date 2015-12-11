# -*- encoding: utf-8 -*-
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from Accounts.models import Log, Usuario
from Empresas.api.filters import EmpresaFilter, EmpleadoFilter, ProcesoFilter
from Empresas.api.pagination import StandardResultsSetPagination
from Empresas.forms import CrearEmpresaForm
from Empresas.models import Empresa, Empleado, Proceso, Perfil, CategoriaProceso, Formato
from Empresas.serializers import EmpresaSerializer, EmpleadoSerializer, ProcesoSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)
    filter_class = EmpresaFilter

    def create(self, request, *args, **kwargs):
        print request.data
        log = Log(user=request.user, actividad='Creacion de Empresa', descripcion='Creacion de Empresa {0} con NIT: {1} '.format(request.data['nombre'], request.data['NIT']))
        log.save()
        return super(EmpresaViewSet,self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        print request.user
        empresa =  self.get_object()
        empresa.active=False
        empresa.save()
        log = Log(user=request.user, actividad='Desactivacion de Empresa', descripcion='Desactivacion de Empresa {0} con NIT: {1} '.format(empresa.nombre, empresa.NIT))
        log.save()
        return Response(status=204)

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


class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)
    filter_class = EmpleadoFilter

    @detail_route(methods=['get'])
    def get_empleados(self, request, id=None):
        print request.data
        queryset = Empleado.objects.filter(perfil__empresa=id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def upload_foto(self, request, id=None):
        empleado=get_object_or_404(Empleado, pk=id)
        file = request.FILES['file']
        from django.conf import settings
        new_path = settings.MEDIA_ROOT
        print new_path
        destination = open(new_path+file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        # do some stuff with uploaded file
        print file
        return Response(status=204)


    def perform_create(self, serializer):
        print(self.request.data)
        print self.request.data['identificacion']
        user = User(username=self.request.data['identificacion'], email=self.request.data['email'])
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        usuario=Usuario(user=user)
        usuario.save()
        # send_mail('New User Huella Gestion', 'Here is the password: {0}.'.format(password), 'linglung1047@gmail.com',
        #     [self.request.data['email']], fail_silently=False)
        perfil=Perfil.objects.get(id=self.request.data['perfil'])
        serializer.save(usuario=usuario, perfil=perfil)

class ProcesoViewSet(viewsets.ModelViewSet):
    serializer_class = ProcesoSerializer
    queryset = Proceso.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)
    filter_class = ProcesoFilter

    @detail_route(methods=['get'])
    def get_procesos(self, request, id=None):
        print request.data
        queryset = Proceso.objects.filter(categoria__empresa=id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.data)
        print(request.data['formatos_asignados'])

        if request.data['categoria']:
            categoria=get_object_or_404(CategoriaProceso.objects.filter(active=True), pk=request.data['categoria'])
            try:
                Proceso.objects.get(active=True, codigo=request.data['codigo'])
            except Proceso.DoesNotExist:
                proceso = Proceso(nombre=request.data['nombre'], descripcion=request.data['descripcion'], codigo=request.data['codigo'], categoria=categoria)
                proceso.save()
                for fa in request.data['formatos_asignados']:
                    print fa
                    formato=Formato.objects.get(id=fa)
                    proceso.formatos_asignados.add(formato)
                    proceso.save()
                serializer = ProcesoSerializer(proceso)
                return Response(serializer.data)

        return Response(status=202)
