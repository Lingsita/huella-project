# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0034_auto_20160605_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoLog',
            fields=[
                ('documento_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Empresas.Documento')),
                ('fecha_creacion', models.DateTimeField(default=datetime.datetime.now)),
            ],
            bases=('Empresas.documento',),
        ),
    ]
