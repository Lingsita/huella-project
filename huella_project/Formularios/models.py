from django.db import models

# Create your models here.
class Formulario(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    descripcion = models.CharField(max_length=200, null=False, blank=True)
    active=models.BooleanField(null=False, default=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)


class Campo(models.Model):
    id_campo = models.CharField(max_length=150, null=False)
    nombre = models.CharField(max_length=150, null=False)
    descripcion= models.CharField(max_length=150)
    tipo=models.CharField(max_length=150, null=False, blank=False, default="text")
    max=models.IntegerField(null=True, blank=True)
    min=models.IntegerField(null=True, blank=True)
    formulario= models.ForeignKey(Formulario)
    active=models.BooleanField(null=False, default=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)








