# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0016_formato_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='tipo_documento',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
