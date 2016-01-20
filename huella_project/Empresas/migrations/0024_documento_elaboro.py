# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0023_auto_20160113_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='elaboro',
            field=models.ForeignKey(to='Empresas.Empleado', null=True),
        ),
    ]
