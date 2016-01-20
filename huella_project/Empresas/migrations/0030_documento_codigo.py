# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0029_documento_is_external'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='codigo',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
