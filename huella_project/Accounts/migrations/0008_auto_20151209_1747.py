# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_auto_20151209_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='change_password_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'change password date'),
        ),
    ]
