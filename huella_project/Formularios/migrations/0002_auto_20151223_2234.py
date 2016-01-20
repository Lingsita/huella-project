# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formularios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formulario',
            name='url',
        ),
        migrations.AddField(
            model_name='campo',
            name='formulario',
            field=models.ForeignKey(default=1, to='Formularios.Formulario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campo',
            name='max',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='campo',
            name='min',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='campo',
            name='tipo',
            field=models.CharField(default=b'text', max_length=150),
        ),
    ]
