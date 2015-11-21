from django.contrib import admin
from Empresas.models import *
# Register your models here.

class PruebaAdmin(admin.ModelAdmin):
    list_display=['nombre','NIT','active']

admin.site.register(Empresa, PruebaAdmin)
admin.site.register(Perfil)
admin.site.register(Empleado)
admin.site.register(CategoriaProceso)
admin.site.register(Proceso)
admin.site.register(Formato)
admin.site.register(Documento)
admin.site.register(Tarea)
