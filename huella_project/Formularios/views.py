from django.shortcuts import render

# Create your views here.
from django.views.generic.simple import direct_to_template
from django.forms import forms, fields

def montar_formulario_dinamico(request):
    campos_dinamicos = {
        'nome': fields.CharField(max_length=100, required=True, label='Nome', initial='Gustavo'),
        'idade': fields.IntegerField(label='Idade', min_value=0),
        'email': fields.EmailField(max_length=200, required=False, label='E-mail')
    }

    FormDinamico = type('', (forms.Form,), campos_dinamicos)
    form = FormDinamico()

    return direct_to_template(request, 'formulario.html', extra_context={'formulario': form})