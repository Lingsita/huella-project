# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import Empresas.models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0020_auto_20151223_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='documento',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='version',
        ),
        migrations.AddField(
            model_name='documento',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='archivo',
            field=models.FileField(null=True, upload_to=Empresas.models.get_file_path, blank=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='external_link',
            field=models.CharField(max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='fecha_emision',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='documento',
            name='formato_default',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='paginas',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='restringido',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='documento',
            name='ubicacion_original',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
