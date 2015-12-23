from Empresas.models import Perfil, CategoriaProceso, Formato

__author__ = 'linglung'

from django import forms
from .models import Empresa, Empleado, Proceso
from datetime import datetime

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
        ('Cedula de ciudadania','Cedula de Ciudadania'),
        ('Cedula de Extranjeria', 'Cedula de Extranjeria'),
        ('Pasaporte', 'Pasaporte')
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
        perfiles= Perfil.objects.filter(empresa=empresa, active=True)
        print(empresa)
        super(CrearEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfiles, widget=forms.Select(attrs={'ng-model':'datos.perfil'}))

class ModificarEmpleadoForm(forms.ModelForm):
    ID_CHOICES={
        ('Cedula de ciudadania','Cedula de Ciudadania'),
        ('Cedula de Extranjeria', 'Cedula de Extranjeria'),
        ('Pasaporte', 'Pasaporte')
    }
    perfil = forms.CharField(max_length=3, widget=forms.Select(attrs={'ng-model':'current_empleado.perfil'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'required':'required', 'ng-model':'current_empleado.email'}))
    tipo_documento = forms.CharField(max_length=150, widget=forms.Select( choices=ID_CHOICES, attrs={'ng-model':'current_empleado.tipo_documento'}))
    class Meta:
        model = Empleado
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.nombre'}),
            'apellido': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.apellido'}),
            'identificacion': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.identificacion'}),
            'direccion': forms.Textarea(attrs={'required':'required', 'ng-model':'current_empleado.direccion'}),
            'codigo': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.codigo'}),
            'telefono1': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.telefono1'}),
            'telefono2': forms.TextInput(attrs={'required':'required', 'ng-model':'current_empleado.telefono2'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        perfiles= Perfil.objects.filter(empresa=empresa, active=True)
        print(empresa)
        super(ModificarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfiles, widget=forms.Select(attrs={'ng-model':'current_empleado.perfil'}))


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
        categorias= CategoriaProceso.objects.filter(empresa=empresa, active=True)
        formatos= Formato.objects.filter(empresa=empresa, active=True)
        super(CrearProcesoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=categorias, widget=forms.Select(attrs={'ng-model':'datos.categoria'}))
        self.fields['formatos_asignados'] = forms.ModelMultipleChoiceField(queryset=formatos, widget=forms.CheckboxSelectMultiple)

class ModificarProcesoForm(forms.ModelForm):

    current_proceso_categoria = forms.CharField(required=True, max_length=3, widget=forms.Select(attrs={'ng-model':'current_proceso.categoria'}))
    current_proceso_formatos_asignados = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Proceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'current_proceso.nombre'}),
            'codigo': forms.TextInput(attrs={'required':'required', 'ng-model':'current_proceso.codigo'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'current_proceso.descripcion'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        categorias= CategoriaProceso.objects.filter(empresa=empresa, active=True)
        formatos= Formato.objects.filter(empresa=empresa, active=True)
        super(ModificarProcesoForm, self).__init__(*args, **kwargs)
        self.fields['current_proceso_categoria'] = forms.ModelChoiceField(queryset=categorias, widget=forms.Select(attrs={'ng-model':'current_proceso.categoria'}))
        self.fields['current_proceso_formatos_asignados'] = forms.ModelMultipleChoiceField(queryset=formatos, widget=forms.SelectMultiple(attrs={'ng-model':'current_proceso.formatos_asignados'}))

class CrearCategoriaProcesoForm(forms.ModelForm):

    categoria_empresa= forms.CharField(required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'categoria.empresa'})),

    class Meta:
        model = CategoriaProceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'categoria.nombre'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'categoria.descripcion'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        super(CrearCategoriaProcesoForm, self).__init__(*args, **kwargs)
        self.fields['categoria_empresa'] = forms.CharField(initial=empresa.pk,required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'categoria.empresa'}))

class CrearTareaForm(forms.ModelForm):

    empleado= forms.CharField(required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'tarea.empleado'}))
    fecha_fin= forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'required':'required', 'ng-model':'tarea.fecha_fin'}))
    perfil = forms.CharField(required=True, max_length=3, widget=forms.Select(attrs={'ng-model':'tarea.perfil'}))

    class Meta:
        model = CategoriaProceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'tarea.nombre'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'tarea.descripcion'}),
            'fecha_fin': forms.TextInput(attrs={'required':'required', 'ng-model':'tarea.fecha_fin'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        perfiles=Perfil.objects.filter(empresa=empresa, active=True)
        super(CrearTareaForm, self).__init__(*args, **kwargs)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfiles, widget=forms.Select(attrs={'ng-model':'tarea.perfil', 'ng-change':'getEmpleadoAutocomplete()'}))

        self.fields['fecha_fin']= forms.DateTimeField(initial=datetime.now, widget=forms.TextInput(attrs={'required':'required', 'ng-model':'tarea.fecha_fin'}))

class ModificaTareaForm(forms.ModelForm):

    empleado= forms.CharField(required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'current_tarea.empleado'}))
    current_fecha_fin= forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'required':'required', 'ng-model':'current_tarea.fecha_fin'}))
    perfil = forms.CharField(required=True, max_length=3, widget=forms.Select(attrs={'ng-model':'tarea.perfil'}))

    class Meta:
        model = CategoriaProceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'current_tarea.nombre'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'current_tarea.descripcion'}),
            'current_fecha_fin': forms.TextInput(attrs={'required':'required', 'ng-model':'current_tarea.fecha_fin'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        perfiles=Perfil.objects.filter(empresa=empresa, active=True)
        super(ModificaTareaForm, self).__init__(*args, **kwargs)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfiles, widget=forms.Select(attrs={'ng-model':'current_tarea.perfil', 'ng-change':'getEmpleadoAutocompleteM()'}))
        self.fields['fecha_fin']= forms.DateTimeField(initial=datetime.now, widget=forms.TextInput(attrs={'required':'required', 'ng-model':'current_tarea.fecha_fin'}))


class CrearPerfilForm(forms.ModelForm):

    procesos = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple())
    formatos_asignados_perfil = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple())
    empresa= forms.CharField(required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'datos.empresa'})),

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
        procesos= Proceso.objects.filter(categoria__empresa=empresa, active=True)
        formatos= Formato.objects.filter(empresa=empresa, active=True)
        super(CrearPerfilForm, self).__init__(*args, **kwargs)
        self.fields['empresa'] = forms.CharField(initial=empresa.pk,required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'datos.empresa'}))
        self.fields['procesos'] = forms.ModelMultipleChoiceField(queryset=procesos)
        self.fields['formatos_asignados_perfil'] = forms.ModelMultipleChoiceField(queryset=formatos)

class ModificarPerfilForm(forms.ModelForm):

    current_perfil_procesos = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple())
    current_perfil_formatos_asignados = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple())
    empresa= forms.CharField(required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'current_perfil.empresa'})),

    class Meta:
        model = Proceso
        fields = '__all__'
        exclude=['active']

        widgets = {
            'nombre': forms.TextInput(attrs={'required':'required', 'ng-model':'current_perfil.nombre'}),
            'codigo': forms.TextInput(attrs={'required':'required', 'ng-model':'current_perfil.codigo'}),
            'descripcion': forms.Textarea(attrs={'required':'required', 'ng-model':'current_perfil.descripcion'})
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        procesos= Proceso.objects.filter(categoria__empresa=empresa, active=True)
        formatos= Formato.objects.filter(empresa=empresa, active=True)
        super(ModificarPerfilForm, self).__init__(*args, **kwargs)
        self.fields['empresa'] = forms.CharField(initial=empresa.pk,required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'current_perfil.empresa'}))
        self.fields['current_perfil_procesos'] = forms.ModelMultipleChoiceField(queryset=procesos, widget=forms.SelectMultiple(attrs={'ng-model':'current_perfil.procesos'}))
        self.fields['current_perfil_formatos_asignados'] = forms.ModelMultipleChoiceField(queryset=formatos, widget=forms.SelectMultiple(attrs={'ng-model':'current_perfil.formatos_asignados'}))





