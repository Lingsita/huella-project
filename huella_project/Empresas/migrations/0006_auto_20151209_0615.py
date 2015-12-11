# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import Empresas.models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0005_auto_20151002_1656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empresa',
            options={'verbose_name': 'Empresa'},
        ),
        migrations.AddField(
            model_name='empleado',
            name='foto',
            field=models.FileField(null=True, upload_to=Empresas.models.get_image_path, blank=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='NIT',
            field=models.CharField(unique=True, max_length=150, verbose_name=b'NIT o Identificacion'),
        ),
    ]
