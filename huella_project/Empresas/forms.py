from Empresas.models import Perfil, CategoriaProceso, Formato

__author__ = 'linglung'

from django import forms
from .models import Empresa, Empleado, Proceso

perfiles=[]

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

class CrearEmpleadoForm(forms.ModelForm):
    ID_CHOICES={
        ('cedula_ciudadania','Cedula de Ciudadania'),
        ('cedula_extranjeria', 'Cedula de Extranjeria'),
        ('pasaporte', 'Pasaporte')
    }
    perfil = forms.CharField(max_length=3, widget=forms.Select(attrs={'ng-model':'datos.perfil'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'required':'required', 'ng-model':'datos.email'}))
    tipo_documento = forms.CharField(max_length=150, widget=forms.Select( choices=ID_CHOICES, attrs={'ng-model':'datos.tipo_documento'}))
    class Meta:
        model = Empleado
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.nombre'}),
            'apellido': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.apellido'}),
            'identificacion': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.identificacion'}),
            'direccion': forms.Textarea(attrs={'required':'required', 'ng-model':'datos.direccion'}),
            'codigo': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.codigo'}),
            'telefono1': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.telefono1'}),
            'telefono2': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.telefono2'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        perfiles= Perfil.objects.filter(empresa=empresa)
        print(empresa)
        super(CrearEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfiles, widget=forms.Select(attrs={'ng-model':'datos.perfil'}))


class CrearProcesoForm(forms.ModelForm):

    categoria = forms.CharField(required=True, max_length=3, widget=forms.Select(attrs={'ng-model':'datos.categoria'}))
    formatos_asignados = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Proceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.nombre'}),
            'codigo': forms.TextInput(attrs={'required':'required', 'ng-model':'datos.codigo'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'datos.descripcion'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        categorias= CategoriaProceso.objects.filter(empresa=empresa)
        formatos= Formato.objects.filter(empresa=empresa)
        print(empresa)
        super(CrearProcesoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=categorias, widget=forms.Select(attrs={'ng-model':'datos.categoria'}))
        self.fields['formatos_asignados'] = forms.ModelMultipleChoiceField(queryset=formatos, widget=forms.CheckboxSelectMultiple)


