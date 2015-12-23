# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0015_perfil_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='formato',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
