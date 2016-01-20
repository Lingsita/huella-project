# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0019_auto_20151223_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formato',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
