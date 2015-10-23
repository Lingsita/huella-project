from django.db import models

# Create your models here.
class Formulario(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    url= models.CharField(max_length=150)
    active=models.BooleanField(null=False, default=True)

class Campo(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    descripcion= models.CharField(max_length=150)
    active=models.BooleanField(null=False, default=True)

class Registro(models.Model):
    campo = models.ForeignKey(Campo)
    valor = models.CharField(max_length=150)
    active=models.BooleanField(null=False, blank=False, default=True)
