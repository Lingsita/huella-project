# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0027_remove_documento_proceso'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='proceso',
            field=models.ForeignKey(default=13, to='Empresas.Proceso'),
            preserve_default=False,
        ),
    ]
