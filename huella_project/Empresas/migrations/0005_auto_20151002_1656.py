# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0004_empresa_nit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='formulario',
            new_name='formato',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='tipo',
        ),
        migrations.AddField(
            model_name='empresa',
            name='email',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono1',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono2',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
