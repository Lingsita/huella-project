# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0033_auto_20160222_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='valor',
            field=models.CharField(max_length=255),
        ),
    ]
