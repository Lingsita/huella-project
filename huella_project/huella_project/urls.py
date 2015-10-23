from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin_site'),
    url(r'^$', 'Accounts.views.index', name ='index'),
    url(r'^accounts/', include('Accounts.urls',  namespace='accounts', app_name='Accounts')),
    url(r'^empresas/', include('Empresas.urls',  namespace='empresas', app_name='Empresas')),
    url(r'^employee$', TemplateView.as_view(template_name="empleado.html")),
    url(r'^prueba/perfil', TemplateView.as_view(template_name="perfil.html")),
    # url(r'^', index, name ='index'),
    # url(r'^login/', Accounts.views.inicio_sesion, name ='inicio_sesion'),
    # url(r'^', 'Accounts.views.inicio_sesion', name ='inicio_sesion'),


]
