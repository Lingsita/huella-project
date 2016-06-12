# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0035_documentolog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentolog',
            name='documento_ptr',
        ),
        migrations.AddField(
            model_name='documento',
            name='is_history_log',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='DocumentoLog',
        ),
    ]
