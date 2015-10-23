from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime


class Usuario(models.Model):
    #model for user account
    user = models.ForeignKey(User)
    change_password_date = models.DateTimeField('change password date')
    superuser = models.BooleanField(null=False, blank=False, default=False)

class Permiso(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    url= models.CharField(max_length=150)
    active=models.BooleanField(null=False, blank=False, default=True)

class Log(models.Model):
    user = models.ForeignKey(User)
    actividad = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)
    date = models.DateTimeField()

class UserSession(models.Model):
    user=models.ForeignKey(User)
    ip=models.CharField(max_length=255)
    date_joined=models.DateTimeField(default=datetime.now, blank=True)
    active=models.BooleanField(default=False)
