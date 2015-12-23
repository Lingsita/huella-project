# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0013_perfil_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'verbose_name_plural': 'Perfiles'},
        ),
        migrations.AddField(
            model_name='perfil',
            name='descripcion',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='formatos_asignados',
            field=models.ManyToManyField(to='Empresas.Formato', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='procesos',
            field=models.ManyToManyField(to='Empresas.Proceso', blank=True),
        ),
    ]
