# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-09-17 07:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_user_provision', '0002_auto_20180917_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rotatingprovisionkey',
            name='rotation_period',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
