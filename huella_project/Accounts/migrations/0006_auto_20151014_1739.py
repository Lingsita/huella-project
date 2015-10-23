# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_auto_20151014_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
