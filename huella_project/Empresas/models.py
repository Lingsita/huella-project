# -*- encoding: utf-8 -*-
from django.db import models

# Create your models here.
from Accounts.models import Usuario
from Formularios.models import Registro, Formulario

import os

def get_image_path(instance, filename):
    return os.path.join('user_fotos', str(instance.id), filename)

class Empresa(models.Model):
    permissions={
        'delete','delete empresa'
    }
    nombre = models.CharField(max_length=150, null=False)
    direccion= models.CharField(max_length=150)
    NIT=models.CharField(max_length=150, unique=True, verbose_name="NIT o Identificacion")
    telefono1=models.CharField(max_length=20, blank=True)
    telefono2=models.CharField(max_length=20, blank=True)
    email=models.CharField(max_length=150, blank=True)
    active=models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'Empresa'
    def __unicode__(self):
        return u'{0}'.format(self.nombre)

class Perfil(models.Model):
    #model for user account
    nombre= models.CharField(max_length=150, null=True)
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Empleado(models.Model):
    usuario = models.ForeignKey(Usuario)
    nombre=models.CharField(max_length=150)
    apellido=models.CharField(max_length=150)
    identificacion=models.CharField(max_length=150)
    perfil = models.ForeignKey(Perfil)
    direccion = models.CharField(max_length=150)
    codigo = models.CharField(max_length=150)
    foto= models.FileField(upload_to=get_image_path, blank=True, null=True)
    telefono1= models.CharField(max_length=20, blank=True)
    telefono2= models.CharField(max_length=20, blank=True)
    is_admin=models.BooleanField(default=False)
    active=models.BooleanField(null=False, blank=False, default=True)

    def __unicode__(self):
        return u'%s %s' % (self.nombre, self.apellido)

class CategoriaProceso(models.Model):
    nombre = models.CharField(max_length=150)
    empresa = models.ForeignKey(Empresa)
    active = models.BooleanField(null=False, blank=False, default=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Formato(models.Model):
    formulario=models.ForeignKey(Formulario)
    descripcion=models.CharField(max_length=150)
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return u'%s' % (self.descripcion)

class Proceso(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    codigo = models.CharField(max_length=150, default=0)
    categoria = models.ForeignKey(CategoriaProceso)
    descripcion = models.CharField(max_length=150)
    formatos_asignados = models.ManyToManyField(Formato)
    active=models.BooleanField(null=False, blank=False, default=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Documento(models.Model):
    formato = models.CharField(max_length=150, null=False)
    proceso= models.CharField(max_length=150)
    registro=models.ManyToManyField(Registro)
    fecha= models.DateTimeField()
    version= models.CharField(max_length=150)
    def __unicode__(self):
        return u'%s %s' % (self.nombre, self.apellido)

class Tarea(models.Model):
    empleado=models.ForeignKey(Empleado)
    nombre = models.CharField(max_length=150, null=False)
    descripcion= models.CharField(max_length=150)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    active=models.BooleanField(null=False, blank=False, default=True)
    def __unicode__(self):
        return u'%s %s' % (self.nombre)
