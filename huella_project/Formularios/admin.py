from django.contrib import admin
from Formularios.models import *
# Register your models here.
class FormularioAdmin(admin.ModelAdmin):
    list_display=['nombre', 'descripcion', 'active']

class CampoAdmin(admin.ModelAdmin):
    list_display=['nombre','tipo','descripcion','formulario', 'active']

admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Campo, CampoAdmin)



