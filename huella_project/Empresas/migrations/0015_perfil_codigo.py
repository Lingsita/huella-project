# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0014_auto_20151214_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='codigo',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
