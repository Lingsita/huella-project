# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0030_documento_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='desc_cambios',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]
