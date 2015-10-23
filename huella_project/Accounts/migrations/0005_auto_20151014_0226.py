# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_auto_20151014_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='date_joined',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
