from django.contrib import admin
from Accounts.models import Usuario, Permiso, Log

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Permiso)
admin.site.register(Log)