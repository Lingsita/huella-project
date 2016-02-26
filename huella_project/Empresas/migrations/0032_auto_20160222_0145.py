# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0031_documento_desc_cambios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='external_link',
            field=models.CharField(max_length=254, null=True, blank=True),
        ),
    ]
