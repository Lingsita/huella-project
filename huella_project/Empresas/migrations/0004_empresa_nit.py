# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0003_auto_20150906_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='NIT',
            field=models.CharField(default=1234567890, max_length=150),
            preserve_default=False,
        ),
    ]
