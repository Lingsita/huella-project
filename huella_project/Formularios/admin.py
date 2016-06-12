from django.contrib import admin
from Formularios.models import *
from django import forms


# Register your models here.
class TipoForm(forms.ModelForm):
    MY_CHOICES = (
        ('text', 'Texto'),
        ('number', 'Numero'),
        ('checkbox', 'Campo de Seleccion'),
        ('textarea', 'Area de texto'),
        ('radio', 'Boton de radio'),
        ('date', 'Fecha'),
    )

    tipo = forms.ChoiceField(choices=MY_CHOICES)

class CampoInlineAdmin(admin.TabularInline):
    extra = 0
    model = Campo
    fields = ('nombre', 'tipo', 'descripcion', 'active')
    form = TipoForm


class FormularioAdmin(admin.ModelAdmin):
    inlines = [CampoInlineAdmin]
    list_display=['nombre', 'descripcion', 'active']


class CampoAdmin(admin.ModelAdmin):
    list_display=['nombre','tipo','descripcion','formulario', 'active']

admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Campo, CampoAdmin)



