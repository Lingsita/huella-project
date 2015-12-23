from django.shortcuts import render

# Create your views here.
from django.forms import forms, fields

def montar_formulario_dinamico(request):
    campos_dinamicos = {
        'nombre': fields.CharField(max_length=100, required=True, label='Nombre', initial='Gustavo'),
        'edad': fields.IntegerField(label='Edad', min_value=0),
        'email': fields.EmailField(max_length=200, required=False, label='E-mail')
    }

    FormDinamico = type('', (forms.Form,), campos_dinamicos)
    form = FormDinamico()

    return render(request, 'formularios.html', {'formulario': form})

def index_formularios(request):

    return render(request, 'formularios.html', {})

def nuevo_formato(request):
    return render(request, 'nuevo_formulario.html', {})