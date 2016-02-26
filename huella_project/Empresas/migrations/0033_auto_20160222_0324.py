# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0032_auto_20160222_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='codigo',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
