# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0024_documento_elaboro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='formato',
        ),
    ]
