# -*- encoding: utf-8 -*-
from cgi import escape

from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from xhtml2pdf import pisa

from Empresas.forms import CrearEmpresaForm, CrearEmpleadoForm, CrearProcesoForm, CrearPerfilForm, ModificarPerfilForm, \
    ModificarProcesoForm, ModificarEmpleadoForm, CrearCategoriaProcesoForm, CrearTareaForm, ModificaTareaForm, \
    CrearDocumentoForm, NuevoDocumentoForm, NuevaVersionDocumentoForm
from Empresas.models import Empresa, Formato, Empleado, Proceso, TipoDocumento, CategoriaProceso, Registro, Documento
from Empresas.serializers import EmpresaSerializer, FormatosSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
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

        empleado= Empleado.objects.get(usuario__user=request.user)
        perfil=empleado.perfil
        empresa = empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=id, active=True)
        if request.FILES:
            form = NuevoDocumentoForm(request.POST, files=request.FILES, empresa=empresa, proceso=proceso, perfil=perfil)
        else:
            form = NuevoDocumentoForm(request.POST, empresa=empresa, proceso=proceso, perfil=perfil)

        if form.is_valid():
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
            return redirect('empresas:mostrar_documento', id=documento.codigo)
        else:
            formatos = perfil.formatos_asignados
            tipo_doc = TipoDocumento.objects.filter(active=True)
            print form.errors

            return render(request, 'nuevo_documento.html',
                          {'proceso': proceso, 'default': True, 'formatos': formatos, 'tipo_doc': tipo_doc,
                           'form_default': form})

        return redirect('index')

def nuevo_documento_by_formato(request, proceso=None, id=None):

    if request.method == 'GET':

        empleado= get_object_or_404(Empleado, usuario__user=request.user)
        perfil=empleado.perfil
        empresa=empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=proceso, active=True)
        formatos =  perfil.formatos_asignados
        formato=get_object_or_404(Formato, id=id, active=True)
        formND = NuevoDocumentoForm(empresa=empresa, proceso=proceso, perfil=perfil)
        campos=Campo.objects.filter(formulario=formato.formulario).order_by('id')
        tipo_doc=TipoDocumento.objects.filter(active=True)
        form = InputForm(fields=campos)
        return render(request, 'nuevo_documento.html', {'proceso':proceso, 'formatos': formatos, 'formato': formato, 'formulario': form, 'tipo_doc': tipo_doc, 'form_default': formND})
    else:
        empleado= Empleado.objects.get(usuario__user=request.user)
        perfil=empleado.perfil
        empresa = empleado.perfil.empresa
        proceso=get_object_or_404(Proceso, id=proceso, active=True)
        formato=get_object_or_404(Formato, id=id, active=True)
        form = NuevoDocumentoForm(request.POST, empresa=empresa, proceso=proceso, perfil=perfil)

        if form.is_valid():
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
            return redirect('empresas:mostrar_documento', id=documento.codigo)
        else:
            formatos = perfil.formatos_asignados
            formato = get_object_or_404(Formato, id=id, active=True)
            campos = Campo.objects.filter(formulario=formato.formulario).order_by('id')
            tipo_doc = TipoDocumento.objects.filter(active=True)
            formulario = InputForm(fields=campos)
            print form.errors

            return render(request, 'nuevo_documento.html',
                          {'proceso': proceso, 'formatos': formatos, 'formato': formato, 'formulario': formulario,
                           'tipo_doc': tipo_doc,
                           'form_default': form}
                          )

        return redirect('index')


def mostrar_documento(request, id=None):
    try:
        empleado = Empleado.objects.get(usuario__user=request.user)
        empresa = empleado.perfil.empresa
        documento = Documento.objects.filter(codigo=id, proceso__categoria__empresa=empresa, is_history_log=False, active=True).latest('id')
        registros = Registro.objects.filter(documento=documento, active=True)
        return render(request, 'empleado/mostrar_documento.html', {'documento': documento, 'registros': registros})
    except Documento.DoesNotExist:
        return redirect('index')


def nueva_version_documento(request, id=None):

    if request.method == 'GET':
        empleado= Empleado.objects.get(usuario__user=request.user)
        empresa = empleado.perfil.empresa
        try:
            documento = Documento.objects.filter(codigo=id, proceso__categoria__empresa=empresa, active=True).latest('id')
        except Documento.DoesNotExist:
            raise Http404
        proceso=documento.proceso
        formND = NuevaVersionDocumentoForm(documento=documento)
        if documento.formato is not None:
            campos = Campo.objects.filter(formulario=documento.formato.formulario).order_by('id')
            registros = Registro.objects.filter(documento=documento)
            formulario = InputForm(fields=campos, registros=registros)
            return render(request, 'empleado/nueva_version_documento.html',
                          {'current_document': documento, 'proceso': proceso, 'form_default': formND, 'formulario': formulario})
        return render(request, 'empleado/nueva_version_documento.html',
                      {'current_document': documento, 'proceso':proceso, 'form_default': formND})
    else:

        empleado= Empleado.objects.get(usuario__user=request.user)
        empresa = empleado.perfil.empresa
        try:
            documento = Documento.objects.filter(codigo=id, proceso__categoria__empresa=empresa, active=True).latest('id')
        except Documento.DoesNotExist:
            raise Http404
        proceso = documento.proceso
        if request.FILES:
            form = NuevaVersionDocumentoForm(request.POST, files=request.FILES, documento=documento)
        else:
            form = NuevaVersionDocumentoForm(request.POST, documento=documento)

        if form.is_valid():
            documento = form.save(documento=documento, empleado=empleado)
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
            return redirect('empresas:mostrar_documento', id=documento.codigo)
        else:
            print form.errors
            return render(request, 'empleado/nueva_version_documento.html',
                          {'current_document': documento, 'proceso': proceso, 'form_default': form})

        return redirect('index')

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    import cStringIO as StringIO
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

#Exportar PDF
def exportar_documento_pdf(request):
    results = ["ling", "lung"]
    # Retrieve data or whatever you need
    return render_to_pdf(
        'pdf_report.html',
        {
            'pagesize': 'A4',
            'mylist': results,
        }
    )

class JSONResponse(HttpResponse):
    """
    Another django rest solutions
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

