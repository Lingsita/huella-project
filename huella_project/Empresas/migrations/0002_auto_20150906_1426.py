# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='superuser',
        ),
        migrations.AddField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
