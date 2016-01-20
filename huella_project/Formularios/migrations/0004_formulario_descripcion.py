# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formularios', '0003_campo_id_campo'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='descripcion',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
