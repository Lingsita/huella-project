# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0021_auto_20160113_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='version',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
