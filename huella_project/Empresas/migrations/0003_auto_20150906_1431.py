# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0002_auto_20150906_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='apellido',
            field=models.CharField(default='blank', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='identificacion',
            field=models.CharField(default='blanl', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='nombre',
            field=models.CharField(default='sin nombre', max_length=150),
            preserve_default=False,
        ),
    ]
