__author__ = 'linglung'

from django import forms
from .models import Empresa

class CrearEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude=['active']
        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.nombre'}),
            'NIT': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.NIT'}),
            'direccion': forms.Textarea(attrs={'required':'required', 'ng-model':'datos.direccion'}),
            'telefono1': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.telefono1'}),
            'telefono2': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.telefono2'}),
            'email': forms.EmailInput(attrs={'required':'required', 'ng-model':'datos.email'})
        }





