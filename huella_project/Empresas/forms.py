__author__ = 'linglung'

from django import forms
from .models import Empresa

class CrearEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude=['active']
        widgets = {
            'nombre': forms.TextInput(attrs={}),
            'direccion': forms.Textarea()
        }



