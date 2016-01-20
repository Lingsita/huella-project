# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formularios', '0004_formulario_descripcion'),
        ('Empresas', '0022_documento_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('campo', models.ForeignKey(to='Formularios.Campo')),
            ],
        ),
        migrations.RemoveField(
            model_name='documento',
            name='registro',
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(to='Empresas.TipoDocumento', null=True),
        ),
        migrations.AddField(
            model_name='registro',
            name='documento',
            field=models.ForeignKey(to='Empresas.Documento'),
        ),
    ]
