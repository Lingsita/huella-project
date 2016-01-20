# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0028_documento_proceso'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='is_external',
            field=models.BooleanField(default=False),
        ),
    ]
