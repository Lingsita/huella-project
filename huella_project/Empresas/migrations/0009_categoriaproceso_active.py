# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0008_proceso_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriaproceso',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
