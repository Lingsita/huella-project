# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0007_auto_20151209_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceso',
            name='codigo',
            field=models.CharField(default=0, max_length=150),
        ),
    ]
