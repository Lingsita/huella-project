# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0017_empleado_tipo_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriaproceso',
            name='descripcion',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proceso',
            name='descripcion',
            field=models.CharField(default=b'', max_length=150, blank=True),
        ),
    ]
