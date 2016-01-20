# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formularios', '0002_auto_20151223_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='campo',
            name='id_campo',
            field=models.CharField(default='id_campo', max_length=150),
            preserve_default=False,
        ),
    ]
