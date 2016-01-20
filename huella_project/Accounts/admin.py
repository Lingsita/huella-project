from django.contrib import admin
from Accounts.models import Usuario, Permiso, Log

class UsuarioAdmin(admin.ModelAdmin):
    list_display=['user', 'superuser']
# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Permiso)
admin.site.register(Log)