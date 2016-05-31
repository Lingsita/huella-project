# -*- encoding: utf-8 -*-
from Empresas.models import Perfil, CategoriaProceso, Formato, TipoDocumento, Registro
from Formularios.models import Campo

__author__ = 'linglung'

from django import forms
from .models import Empresa, Empleado, Proceso, Documento
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

class CrearDocumentoForm(forms.ModelForm):

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
        super(CrearDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['empresa'] = forms.CharField(initial=empresa.pk,required=True, widget=forms.HiddenInput(attrs={'required':'required', 'ng-model':'datos.empresa'}))
        self.fields['procesos'] = forms.ModelMultipleChoiceField(queryset=procesos)
        self.fields['formatos_asignados_perfil'] = forms.ModelMultipleChoiceField(queryset=formatos)

class NuevoDocumentoForm(forms.ModelForm):

    CHOICES = (('1', 'Enlace Externo',), ('0', 'Subir Archivo desde este equipo',))
    CHOICES_RESTRINGIDO = (('1', 'Si',), ('0', 'No',))
    formato = forms.CharField(widget=forms.TextInput(attrs={'required': 'required'}))
    formato_default = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'ng-model': 'fields.formato_default'}))
    # elaboro = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'class': 'span6', 'ng-model': 'fields.elaboro'}))
    codigo = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'ng-model': 'fields.codigo'}))
    tipo_documento = forms.ChoiceField(widget=forms.TextInput(attrs={'required': 'required', 'class': 'span6', 'ng-model': 'fields.tipo_documento'}))
    fecha_emision = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'type': 'date', 'ng-model': 'fields.fecha_emision'}))
    paginas = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'ng-model': 'fields.paginas', 'class': 'span6'}))
    external_link = forms.CharField(widget=forms.TextInput(attrs={'ng-model':'fields.external_link', 'ng-required': 'fields.is_external==1', 'class': 'span6', 'placeholder': 'Pega la dirección de enlace aquí.'}))
    is_external = forms.ChoiceField(widget=forms.RadioSelect(attrs={'required': 'required', 'ng-model': 'fields.is_external', 'ng-change': 'tipoArchivo()'}), choices=CHOICES, initial=1)
    archivo = forms.FileField(widget=forms.FileInput(attrs={'ng-required': 'fields.is_external==0', 'style':'visibility:hidden'}))
    restringido = forms.ChoiceField(widget=forms.RadioSelect(attrs={'required': 'required', 'ng-model': 'fields.restringido'}), choices=CHOICES_RESTRINGIDO)
    ubicacion_original = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'required', 'class': 'span6','ng-model': 'fields.ubicacion_original'}))
    version = forms.CharField(widget=forms.TextInput(attrs={'required': 'required', 'class': 'span6', 'ng-model': 'fields.version'}))
    desc_cambios = forms.CharField(widget=forms.Textarea(attrs={'class': 'span6', 'ng-model': 'fields.desc_cambios', 'placeholder': 'Llene este campo en caso de no ser la primera version del documento.'}))

    class Meta:
        model = Documento
        fields = '__all__'
        exclude=['active']

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa')
        proceso = kwargs.pop('proceso')
        perfil = kwargs.pop('perfil')
        categorias = CategoriaProceso.objects.filter(active=True, empresa=empresa)
        procesos= perfil.procesos.filter(active=True, categoria=proceso.categoria)
        tipos_documento=TipoDocumento.objects.filter(active=True)
        super(NuevoDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['paginas'].initial='1'
        self.fields['tipo_documento']=forms.ModelChoiceField(queryset=tipos_documento, widget=forms.Select(attrs={'class':'span6'}))
        self.fields['proceso'] = forms.ModelChoiceField(queryset=procesos, widget=forms.Select(attrs={'class':'span6', 'ng-model':'fields.proceso', 'required':'required'}))
        self.fields['categoria'] = forms.ModelChoiceField(queryset=categorias, widget=forms.Select(attrs={'class':'span6','ng-change':'getProcesosByCategoria()', 'ng-model':'fields.categoria'}))

    def save(self, commit=True, *args, **kwargs):
        results = []
        if 'formato' in kwargs:
            formato = kwargs.pop('formato')
            formato_default = False
        else:
            formato = None
            formato_default = True

        print self.data
        documento = Documento(
            formato=formato,
            formato_default=formato_default,
            proceso=Proceso.objects.get(pk=self.data.get('proceso')),
            elaboro=kwargs.pop('empleado'),
            codigo=self.data.get('codigo'),
            tipo_documento=TipoDocumento.objects.get(pk=self.data.get('tipo_documento')),
            fecha_emision=self.data.get('fecha_emision'),
            paginas=int(self.data.get('paginas')),
            is_external=self.data.get('is_external'),
            restringido=self.data.get('restringido'),
            ubicacion_original=self.data.get('ubicacion_original'),
            version=self.data.get('version'),
            desc_cambios=self.data.get('desc_cambios'),
        )
        for d in self.data:
            ext_link= self.data[d]
            if d == 'external_link':
                ext_link= self.data[d]
                documento.external_link=ext_link

        documento.save()

        if formato is not None:
            form = formato.formulario
            campos = Campo.objects.filter(active=True, formulario=form)
            for campo in campos:

                if campo.nombre in self.data:
                    print "{0} : {1}".format(campo.nombre, self.data.get(campo.nombre, default=None))
                    if campo.tipo == 'radio' or campo.tipo == 'checkbox':
                        valor = 'si'
                    else:
                        valor = self.data.get(campo.nombre, default=None)
                else:
                    valor='no'
                registro = Registro(documento=documento, campo=campo, valor=valor)

        return documento


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





