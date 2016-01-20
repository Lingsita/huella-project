# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0018_auto_20151220_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formato',
            name='active',
            field=models.BooleanField(default=b''),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha_fin',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha_inicio',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
