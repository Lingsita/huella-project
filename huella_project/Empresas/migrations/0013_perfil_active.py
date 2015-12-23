# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0012_formato_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
