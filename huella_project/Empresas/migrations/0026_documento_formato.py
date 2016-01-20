# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0025_remove_documento_formato'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='formato',
            field=models.ForeignKey(to='Empresas.Formato', null=True),
        ),
    ]
