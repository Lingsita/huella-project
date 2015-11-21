from rest_framework.routers import DefaultRouter
from Formularios.api.views import FormularioViewSet

from django.conf.urls import patterns, url, include

router = DefaultRouter()
router.register(r'formulario', FormularioViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    )