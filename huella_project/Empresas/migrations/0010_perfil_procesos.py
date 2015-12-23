# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0009_categoriaproceso_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='procesos',
            field=models.ManyToManyField(to='Empresas.Proceso'),
        ),
    ]
