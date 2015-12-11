# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_auto_20151014_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
