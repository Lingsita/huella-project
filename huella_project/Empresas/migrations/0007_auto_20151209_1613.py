# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0006_auto_20151209_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='telefono1',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='telefono2',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
