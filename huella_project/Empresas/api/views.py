# -*- encoding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions
from Accounts.models import Log, Usuario
from Empresas.api.filters import EmpresaFilter, EmpleadoFilter, ProcesoFilter, PerfilFilter, CategoriaProcesoFilter
from Empresas.api.pagination import StandardResultsSetPagination
from Empresas.forms import CrearEmpresaForm
from Empresas.models import Empresa, Empleado, Proceso, Perfil, CategoriaProceso, Formato, Tarea, Documento
from Empresas.serializers import EmpresaSerializer, EmpleadoSerializer, ProcesoSerializer, PerfilSerializer, \
    CategoriaProcesoSerializer, TareasSerializer, FormatosSerializer, DocumentoSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.
from Empresas.api.permissions import IsBusinessAdmin, IsAdminOrBusinessAdmin
from Formularios.models import Formulario, Campo
from django.conf import settings


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

        form = CrearEmpresaForm()
    return render(request, 'admin_empresas.html', {'form': form})


class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_class = EmpleadoFilter

    @detail_route(methods=['get'])
    def get_empleados(self, request, id=None):
        queryset = Empleado.objects.filter(perfil__empresa=id, active=True).order_by('nombre')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_empleados_by_perfil(self, request, id=None):
        queryset = Empleado.objects.filter(perfil=id, active=True).order_by('nombre')

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
        destination = open(new_path+file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        # do some stuff with uploaded file
        empleado.foto=file
        empleado.save()
        serializer=EmpleadoSerializer(empleado)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print request.data['is_admin']
        empleado= self.get_object()
        empleado.nombre= request.data['nombre']
        empleado.apellido= request.data['apellido']
        user=empleado.usuario.user
        user.email= request.data['email']
        user.save()
        empleado.direccion= request.data['direccion']
        empleado.tipo_documento=request.data['tipo_documento']
        empleado.identificacion= request.data['identificacion']
        empleado.codigo= request.data['codigo']
        empleado.telefono1= request.data['telefono1']
        empleado.telefono2= request.data['telefono2']
        empleado.is_admin=request.data['is_admin']
        empleado.perfil=get_object_or_404(Perfil, id=request.data['perfil'])
        empleado.save()
        serializer=EmpleadoSerializer(empleado)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=self.request.data['identificacion'])
            content = {'message': 'Este Usuario ya existe'}
            return Response(content, status=status.HTTP_302_FOUND)
        except User.DoesNotExist:
            user = User(username=self.request.data['identificacion'], email=self.request.data['email'])
            password = User.objects.make_random_password()
            user.set_password(password)
            user.first_name = self.request.data['nombre']
            user.last_name = self.request.data['apellido']
            user.save()
            usuario=Usuario(user=user)
            usuario.save()

        perfil=Perfil.objects.get(id=self.request.data['perfil'])
        empleado = Empleado(
            usuario=usuario,
            nombre=request.data['nombre'],
            apellido=request.data['apellido'],
            direccion=request.data['direccion'],
            tipo_documento=request.data['tipo_documento'],
            identificacion=request.data['identificacion'],
            codigo=request.data['codigo'],
            telefono1=request.data['telefono1'],
            telefono2=request.data['telefono2'],
            is_admin=request.data['is_admin'],
            perfil=perfil
            )
        print empleado
        empleado.save()
        # send_mail('New User Huella Gestion', ('Here is the password: {0}.').format(password), settings.EMAIL_HOST_USER,
            #     [self.request.data['email']], fail_silently=False)
        log = Log(user=request.user, actividad='Creacion de Empleado', descripcion='Creacion de Empleado {0} en empresa: {1} '.format(empleado.nombre, empleado.perfil.empresa.nombre))

        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        empleado =  self.get_object()
        empleado.active=False
        empleado.save()
        log = Log(user=request.user, actividad='Desactivacion de Empleado', descripcion='Desactivacion de Empleado {0} en empresa: {1} '.format(empleado.nombre, empleado.perfil.empresa.nombre))
        log.save()
        return Response(status=204)

class CategoriaProcesoViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaProcesoSerializer
    queryset = CategoriaProceso.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_class = CategoriaProcesoFilter

    def perform_create(self, serializer):
        print(self.request.data)
        empresa=get_object_or_404(Empresa, pk=self.request.data['empresa'])
        serializer.save(empresa=empresa)

class ProcesoViewSet(viewsets.ModelViewSet):
    serializer_class = ProcesoSerializer
    queryset = Proceso.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_class = ProcesoFilter

    @detail_route(methods=['get'])
    def get_procesos(self, request, id=None):
        queryset = Proceso.objects.filter(categoria__empresa=id, active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def empleado(self, request):

        empleado= Empleado.objects.get(usuario__user=request.user)
        queryset = Proceso.objects.filter(categoria__empresa=empleado.perfil.empresa, active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def procesos_by_category(self, request, id=None):
        print id
        categoria=get_object_or_404(CategoriaProceso, active=True, pk=id)
        print categoria

        empleado= Empleado.objects.get(usuario__user=request.user)
        queryset=empleado.perfil.procesos.filter(categoria=categoria, active=True)
        # queryset = Proceso.objects.filter(categoria=categoria, active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        content={}
        if request.data['categoria']:
            categoria=get_object_or_404(CategoriaProceso.objects.filter(active=True), pk=request.data['categoria'])
            try:
                Proceso.objects.get(active=True, codigo=request.data['codigo'])
                content={
                    'codigo': 'Existe un proceso con este codigo en la empresa'
                }
                return Response(content, status=400)
            except Proceso.DoesNotExist:
                proceso = Proceso(nombre=request.data['nombre'], descripcion=request.data['descripcion'], codigo=request.data['codigo'], categoria=categoria)
                proceso.save()
                for fa in request.data['formatos_asignados']:

                    formato=Formato.objects.get(id=fa)
                    proceso.formatos_asignados.add(formato)
                    proceso.save()
                serializer = ProcesoSerializer(proceso)
                return Response(serializer.data)
        else:
            content={
                'categoria': 'El proceso debe tener una categoria'
            }
        return Response(content, status=400)

    def update(self, request, *args, **kwargs):
        try:
            proceso = get_object_or_404(Proceso, codigo=request.data['codigo'])
            print(request.data)
            return super(ProcesoViewSet,self).update(request, *args, **kwargs)
        except Proceso.DoesNotExist:
            content={
                'codigo': 'Existe un proceso con este codigo en la empresa'
            }
            return Response(content, status=400)

    def destroy(self, request, *args, **kwargs):
        proceso =  self.get_object()
        proceso.active=False
        proceso.save()

        perfiles = Perfil.objects.filter(active=True, empresa=proceso.categoria.empresa)

        for p in perfiles:
            p.procesos.remove(proceso)
            p.save()
        log = Log(user=request.user, actividad='Desactivacion de Proceso', descripcion='Desactivacion de Proceso {0} en empresa: {1} '.format(proceso.nombre, proceso.categoria.empresa.nombre))
        log.save()
        return Response(status=204)

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_class = PerfilFilter

    @detail_route(methods=['get'])
    def get_perfiles(self, request, id=None):

        queryset = Perfil.objects.filter(empresa=id, active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        if request.data['empresa']:
            empresa=get_object_or_404(Empresa.objects.filter(active=True), pk=request.data['empresa'])
            try:
                Perfil.objects.get(active=True, codigo=request.data['codigo'])
                content = {'perfil_exists': 'Ya existe un perfil con este codigo'}
                return Response(content, status=202)
            except Perfil.DoesNotExist:
                perfil = Perfil(nombre=request.data['nombre'], descripcion=request.data['descripcion'], codigo=request.data['codigo'], empresa=empresa)
                perfil.save()

                for fa in request.data['formatos_asignados']:

                    formato=Formato.objects.get(id=fa)
                    perfil.formatos_asignados.add(formato)
                    perfil.save()
                for pr in request.data['procesos']:
                    proceso=Proceso.objects.get(id=pr)
                    perfil.procesos.add(proceso)
                    perfil.save()
                serializer = PerfilSerializer(perfil)
                log = Log(user=request.user, actividad='Creacion de Perfil', descripcion='Creacion de perfil {0} en empresa: {1} '.format(perfil.nombre, perfil.empresa.nombre))
                log.save()
                return Response(serializer.data)

        return Response(status=202)

    def destroy(self, request, *args, **kwargs):
        perfil =  self.get_object()
        perfil.active=False
        perfil.save()
        log = Log(user=request.user, actividad='Desactivacion de Perfil', descripcion='Desactivacion de Perfil {0} en empresa: {1} '.format(perfil.nombre, perfil.empresa.nombre))
        log.save()
        return Response(status=204)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.nombre = request.data['nombre']
        instance.codigo = request.data['codigo']
        instance.descripcion = request.data['descripcion']
        procesos= request.data['procesos']
        formatos_asignados=request.data['formatos_asignados']
        proc=[]
        formas=[]

        for p in procesos:
            ps=Proceso.objects.get(pk=p)
            proc.append(ps)

        for f in formatos_asignados:
            fa=Formato.objects.get(pk=f)
            formas.append(fa)
        instance.procesos=proc
        instance.formatos_asignados=formas
        instance.save()
        serializer=PerfilSerializer(instance)
        return Response(serializer.data)

class TareasViewSet(viewsets.ModelViewSet):
    serializer_class = TareasSerializer
    queryset = Tarea.objects.filter(active=True)
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'])
    def get_tareas(self, request, id=None):
        queryset = Tarea.objects.filter(empleado__perfil__empresa=id, active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        empleado = get_object_or_404(Empleado, pk=self.request.data['empleado'], active=True)
        serializer.save(empleado=empleado)

    def destroy(self, request, *args, **kwargs):
        tarea =  self.get_object()
        tarea.active=False
        tarea.save()
        log = Log(user=request.user, actividad='Desactivacion de Tarea', descripcion='Desactivacion de Tarea {0} {1} asignada a: {2} en empresa: {3} '.format(tarea.nombre, tarea.empleado.nombre,  tarea.empleado.apellido, tarea.empleado.perfil.empresa.nombre))
        log.save()
        return Response(status=204)

    def update(self, request, *args, **kwargs):
        tarea =  self.get_object()
        log = Log(user=request.user, actividad='Modificacion de Tarea', descripcion='Modificacion de Tarea {0} en empresa: {1} '.format(tarea.nombre, tarea.empleado.perfil.empresa.nombre))
        log.save()

        if isinstance(request.data['empleado'], int):
            print('entro a string')
            empleado = get_object_or_404(Empleado, pk=request.data['empleado'], active=True)
            tarea.empleado=empleado
            tarea.fecha_fin=request.data['fecha_fin']
            tarea.nombre=request.data['nombre']
            tarea.descripcion=request.data['descripcion']
            tarea.save()
            serializer=PerfilSerializer(tarea)
            return Response(serializer.data)

        elif request.data['empleado']=="" or request.data['empleado']==None:
            empleado = get_object_or_404(Empleado, pk=self.request.data['empleado'], active=True)
        else:
            return super(TareasViewSet,self).update(request, *args, **kwargs)


class FormatoViewSet(viewsets.ModelViewSet):
    serializer_class = FormatosSerializer
    queryset = Formato.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrBusinessAdmin, )
    # filter_class = FormatoFilter

    def list(self, request):
        try:
            empleado= Empleado.objects.get(usuario__user=request.user)
            empresa=empleado.perfil.empresa
            queryset=Formato.objects.filter(empresa=empresa, active=True)
        except Empleado.DoesNotExist:
            empresa=get_object_or_404(Empresa, id=request.session['empresa'])
            queryset=Formato.objects.filter(empresa=empresa, active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            empleado= Empleado.objects.get(usuario__user=request.user)
            empresa=empleado.perfil.empresa
        except Empleado.DoesNotExist:
             empresa=get_object_or_404(Empresa, id=request.session['empresa'])
        formulario=Formulario(nombre=request.data['nombre'], descripcion=request.data['descripcion'])
        formulario.save()
        formato=Formato(nombre=request.data['nombre'], descripcion=request.data['descripcion'], empresa=empresa, formulario=formulario)
        formato.save()
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

        serializer = FormatosSerializer(formulario)
        return Response(serializer.data)

class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer
    queryset = Documento.objects.all()
    lookup_field = 'id'
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    # def list(self, request):
    #     empleado= Empleado.objects.get(usuario__user=request.user)
    #     queryset=Documento.objects.filter(empleado=empleado, active=True)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)

    @detail_route(methods=['get'])
    def by_proceso(self, request, id=None):

        empleado= Empleado.objects.get(usuario__user=request.user)

        proceso=get_object_or_404(Proceso, pk=id, active=True)

        queryset=Documento.objects.filter(elaboro=empleado, proceso=proceso, active=True)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

