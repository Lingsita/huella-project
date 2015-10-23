# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('emisor', models.ForeignKey(related_name='chat_emisor', to=settings.AUTH_USER_MODEL)),
                ('receptor', models.ForeignKey(related_name='chat_receptor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
