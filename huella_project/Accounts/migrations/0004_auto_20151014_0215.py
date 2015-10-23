# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_usersession_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='ip',
            field=models.CharField(max_length=255),
        ),
    ]
