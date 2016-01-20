# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0023_auto_20160113_2148'),
        ('Formularios', '0004_formulario_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='campo',
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
    ]
