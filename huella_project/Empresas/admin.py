from django.contrib import admin
from Empresas.models import *
# Register your models here.

class PruebaAdmin(admin.ModelAdmin):
    list_display=['nombre','NIT','active']

class PerfilAdmin(admin.ModelAdmin):
    list_display=['nombre','descripcion','empresa','active']

class DocumentoAdmin(admin.ModelAdmin):
    list_display=['formato','proceso','elaboro','tipo_documento', 'active']

admin.site.register(Empresa, PruebaAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Empleado)
admin.site.register(CategoriaProceso)
admin.site.register(Proceso)
admin.site.register(Formato)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(TipoDocumento)
admin.site.register(Registro)
admin.site.register(Tarea)
