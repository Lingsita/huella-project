# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0011_perfil_formatos_asignados'),
    ]

    operations = [
        migrations.AddField(
            model_name='formato',
            name='nombre',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
