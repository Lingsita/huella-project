# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from Empresas.forms import CrearEmpresaForm, CrearEmpleadoForm, CrearProcesoForm, CrearPerfilForm, ModificarPerfilForm, \
    ModificarProcesoForm, ModificarEmpleadoForm, CrearCategoriaProcesoForm, CrearTareaForm, ModificaTareaForm, \
    CrearDocumentoForm, NuevoDocumentoForm
from Empresas.models import Empresa, Formato, Empleado, Proceso, TipoDocumento, CategoriaProceso, Registro, Documento
from Empresas.serializers import EmpresaSerializer, FormatosSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from Formularios.models import Formulario, Campo
from Formularios.views import InputForm

#forms
from django.shortcuts import render, get_object_or_404
from django import forms
from django.forms import fields
from Formularios.models import Formulario, Campo
import time


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

def empresa_detail(request, id):

    try:
        empresa = Empresa.objects.get(id=id)
        request.session['empresa']=empresa.id
        form_procesos=CrearProcesoForm(empresa=empresa)
        form_empleados=CrearEmpleadoForm(empresa=empresa)
        form_perfiles=CrearPerfilForm(empresa=empresa)
        form_mp = ModificarPerfilForm(empresa=empresa)
        form_mpro = ModificarProcesoForm(empresa=empresa)
        form_mempleado = ModificarEmpleadoForm(empresa=empresa)
        form_categoria = CrearCategoriaProcesoForm(empresa=empresa)
        form_tarea = CrearTareaForm(empresa=empresa)
        form_mtarea = ModificaTareaForm(empresa=empresa)
        return render(request, 'empresa.html', {'empresa':empresa, 'form_empleados':form_empleados, 'form_procesos':form_procesos, 'form_perfiles':form_perfiles, 'form_mp':form_mp, 'form_mpro':form_mpro, 'form_mempleado':form_mempleado, 'form_categoria':form_categoria, 'form_tarea':form_tarea, 'form_mtarea':form_mtarea})
    except Empresa.DoesNotExist:
        return redirect('/empresas')

def admin_empresa_detail(request):
    print('edd')

    try:
        print('edd')
        empleado=Empleado.objects.get(usuario__user=request.user)
        empresa = empleado.perfil.empresa
        form_procesos=CrearProcesoForm(empresa=empresa)
        form_empleados=CrearEmpleadoForm(empresa=empresa)
        form_perfiles=CrearPerfilForm(empresa=empresa)
        form_mp = ModificarPerfilForm(empresa=empresa)
        form_mpro = ModificarProcesoForm(empresa=empresa)
        form_mempleado = ModificarEmpleadoForm(empresa=empresa)
        form_categoria = CrearCategoriaProcesoForm(empresa=empresa)
        form_tarea = CrearTareaForm(empresa=empresa)
        form_mtarea = ModificaTareaForm(empresa=empresa)
        return render(request, 'empresa.html', {'empresa':empresa, 'form_empleados':form_empleados, 'form_procesos':form_procesos, 'form_perfiles':form_perfiles, 'form_mp':form_mp, 'form_mpro':form_mpro, 'form_mempleado':form_mempleado, 'form_categoria':form_categoria, 'form_tarea':form_tarea, 'form_mtarea':form_mtarea})
    except Empresa.DoesNotExist:
        return redirect('/empresas')


def montar_formulario_dinamico(request, id):

    formulario=get_object_or_404(Formulario, id=id, active=True)
    campos=Campo.objects.filter(formulario=formulario)
    form = InputForm(fields=campos)
    form_base=CrearDocumentoForm()
    return render(request, 'nuevo_documento.html', {'nombre':formulario.nombre, 'form_base':form_base,'descripcion':formulario.descripcion, 'formulario': form})

def nuevo_documento(request, id=None):
    if request.method == 'GET':
        empleado= Empleado.objects.get(usuario__user=request.user)
        perfil=empleado.perfil
        empresa = empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=id, active=True)
        formatos =  perfil.formatos_asignados
        tipo_doc=TipoDocumento.objects.filter(active=True)
        formND = NuevoDocumentoForm(empresa=empresa, proceso=proceso, perfil=perfil)
        return render(request, 'nuevo_documento.html', {'proceso':proceso,'default':True,'formatos': formatos, 'tipo_doc': tipo_doc, 'form_default': formND})
    else:
        print(request.POST['external_link'])
        empleado= Empleado.objects.get(usuario__user=request.user)
        perfil=empleado.perfil
        empresa = empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=id, active=True)
        if request.FILES:
            form = NuevoDocumentoForm(request.POST, files=request.FILES, empresa=empresa, proceso=proceso, perfil=perfil)
        else:
            form = NuevoDocumentoForm(request.POST, empresa=empresa, proceso=proceso, perfil=perfil)

        try:
            documento = form.save(empleado=empleado)
            if request.FILES:
                file = request.FILES['archivo']
                date =  time.strftime("%Y-%m-%d-%H%M%S")
                print date
                from django.conf import settings
                new_path = settings.MEDIA_ROOT+"docs/"
                ext = file.name.split('.')[-1]
                filename = "%s_%s_%s_%s.%s" % ("formato_estandar", documento.proceso.nombre, documento.codigo, date, ext)
                destination = open(new_path+filename, 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                documento.archivo=file
                documento.save()
        except Documento.DoesNotExist:
            return redirect('index')



        return redirect('index')

def nuevo_documento_by_formato(request, proceso=None, id=None):

    if request.method == 'GET':
        print(proceso)
        print(id)

        empleado= get_object_or_404(Empleado,usuario__user=request.user)
        perfil=empleado.perfil
        empresa=empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=proceso, active=True)
        formatos =  perfil.formatos_asignados
        formato=get_object_or_404(Formato, id=id, active=True)
        formND = NuevoDocumentoForm(empresa=empresa, proceso=proceso, perfil=perfil)
        campos=Campo.objects.filter(formulario=formato.formulario)
        tipo_doc=TipoDocumento.objects.filter(active=True)
        form = InputForm(fields=campos)
        return render(request, 'nuevo_documento.html', {'proceso':proceso, 'formatos': formatos, 'formato': formato, 'formulario': form, 'tipo_doc': tipo_doc, 'form_default': formND})
    else:
        print(request.POST['external_link'])
        empleado= Empleado.objects.get(usuario__user=request.user)
        perfil=empleado.perfil
        empresa = empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=proceso, active=True)
        formato=get_object_or_404(Formato, id=id, active=True)
        form = NuevoDocumentoForm(request.POST, empresa=empresa, proceso=proceso, perfil=perfil)
        try:
            documento = form.save(empleado=empleado, formato=formato)

            for f in request.FILES:
                file = request.FILES.get(f)
                date =  time.strftime("%Y-%m-%d-%H%M%S")
                from django.conf import settings
                new_path = settings.MEDIA_ROOT+"docs/"
                ext = file.name.split('.')[-1]
                filename = "%s_%s_%s_%s.%s" % (documento.formato.nombre, documento.proceso.nombre, documento.codigo, date, ext)

                from django.conf import settings
                new_path = settings.MEDIA_ROOT+"docs/"
                destination = open(new_path+filename, 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                if f == 'archivo':
                    documento.archivo=file
                    documento.save()
                else:
                    campo = Campo.objects.get(id_campo=f)
                    registro = Registro(documento=documento, campo=campo, valor=new_path+file.name)
                    registro.save()
        except Documento.DoesNotExist:
            return redirect('index')

        return redirect('index')

def mostrar_documento(request, id=None):
    try:
        empleado = Empleado.objects.get(usuario=request.user)
        empresa = empleado.perfil.empresa
        documento = Documento.objects.get(codigo=id, empresa=empresa, active=True)
        registros = Registro.objects.filter(documento=documento, active=True)
        return render(request, 'nuevo_documento.html', {'documento': documento, 'registros': registros})

    except Documento.DoesNotExist:
        return redirect('index')

#Another django rest solutions

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

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


def empresa_detail_rest(request, pk):
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


class EmpresasRest(APIView):
    serializer= EmpresaSerializer
    def get(self, request, format=None):
        empresas = Empresa.objects.filter(active=True)
        resp= self.serializer(empresas, many=True)
        return Response(resp.data)
    def post(self, request, format=None):
        empresa= self.serializer(data= request.data)
        if empresa.is_valid():
            empresa.save()
            resp= self.serializer(empresa.data, many=False)
            #return Response(resp.data)
            return JSONResponse(empresa.data)
        else:

            return Response({'message': 'this is my message for fail post'})

empresas_rest= EmpresasRest.as_view()

