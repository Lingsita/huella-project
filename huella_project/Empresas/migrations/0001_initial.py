# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Formularios', '0001_initial'),
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('formulario', models.CharField(max_length=150)),
                ('proceso', models.CharField(max_length=150)),
                ('fecha', models.DateTimeField()),
                ('version', models.CharField(max_length=150)),
                ('tipo', models.CharField(max_length=150)),
                ('registro', models.ManyToManyField(to='Formularios.Registro')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=150)),
                ('is_admin', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('empresa', models.ForeignKey(to='Empresas.Empresa')),
                ('formulario', models.ForeignKey(to='Formularios.Formulario')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('superuser', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(to='Empresas.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(to='Empresas.CategoriaProceso')),
                ('formatos_asignados', models.ManyToManyField(to='Empresas.Formato')),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=150)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('empleado', models.ForeignKey(to='Empresas.Empleado')),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='perfil',
            field=models.ForeignKey(to='Empresas.Perfil'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='usuario',
            field=models.ForeignKey(to='Accounts.Usuario'),
        ),
        migrations.AddField(
            model_name='categoriaproceso',
            name='empresa',
            field=models.ForeignKey(to='Empresas.Empresa'),
        ),
    ]
