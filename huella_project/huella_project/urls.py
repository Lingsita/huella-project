from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from huella_project import settings
from django.conf.urls.static import  static



urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin_site'),
    url(r'^$', 'Accounts.views.index', name ='index'),
    url(r'^accounts/', include('Accounts.urls',  namespace='accounts', app_name='Accounts')),
    url(r'^api-empresas/', include('Empresas.api.urls',  namespace='api_empresas', app_name='api_empresas')),
    url(r'^api/formularios/', include('Formularios.api.urls',  namespace='api_formularios', app_name='api_formularios')),
    url(r'^formularios/', include('Formularios.urls',  namespace='formularios', app_name='formularios')),
    url(r'^', include('Empresas.urls',  namespace='empresas', app_name='Empresas')),
    url(r'^employee$', TemplateView.as_view(template_name="empleado.html")),
    url(r'^prueba/perfil', TemplateView.as_view(template_name="perfil.html")),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)