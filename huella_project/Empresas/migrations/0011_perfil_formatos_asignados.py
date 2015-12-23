# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0010_perfil_procesos'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='formatos_asignados',
            field=models.ManyToManyField(to='Empresas.Formato'),
        ),
    ]
