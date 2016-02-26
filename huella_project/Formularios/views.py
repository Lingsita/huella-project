from django.shortcuts import render, get_object_or_404

# Create your views here.
from django import forms
from django.forms import fields
from Formularios.models import Formulario, Campo

class InputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_fields = kwargs.pop("fields", {})

        super(InputForm, self).__init__(*args, **kwargs)

        for field in form_fields:
            # Get the field attributes
            field_name = field.id_campo
            field_label = field.nombre
            field_type = field.tipo

            # Create the form field
            if field_type == 'number':
                self.fields[field_name] = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'span6'}),required=True, label=field_label)
            elif field_type == 'textarea':
                self.fields[field_name] = forms.CharField(widget=forms.Textarea(attrs={'class':'span6'}), max_length=255,required=True, label=field_label)
            elif field_type == 'checkbox':
                self.fields[field_name] = forms.ChoiceField(widget=forms.CheckboxInput, required=True, label=field_label)
            elif field_type == 'radio':
                CHOICES = ((field.id_campo, field.nombre),)
                self.fields[field_name] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True, label=field_label, help_text='radio')
            elif field_type == 'date':
                self.fields[field_name] = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=True, label=field_label, help_text='date')
            elif field_type == 'file':
                self.fields[field_name] = forms.FileField(widget=forms.FileInput(attrs={'type':'file', 'ng-model': field.id_campo, 'style': 'visibility:hidden', 'onchange': "visibleFileValue('"+field.id_campo+"')"}), required=True, label=field_label, help_text='file')
            else:
                self.fields[field_name] = forms.CharField(widget=forms.TextInput(attrs={'class':'span6'}),max_length=100, required=True, label=field_label)


def montar_formulario_dinamico(request, id):

    formulario=get_object_or_404(Formulario, id=id, active=True)
    campos=Campo.objects.filter(formulario=formulario)
    form = InputForm(fields=campos)
    return render(request, 'ver_formulario.html', {'nombre':formulario.nombre, 'descripcion':formulario.descripcion, 'formulario': form})


def index_formularios(request):
    return render(request, 'formularios.html', {})

def nuevo_formulario(request):
    return render(request, 'nuevo_formulario.html', {})

def index_formatos(request):
    return render(request, 'formatos.html', {})

def nuevo_formato(request):
    return render(request, 'nuevo_formato.html', {})