# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-09-14 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RotatingProvisionKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('issue_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('rotation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('rotation_period', models.DurationField()),
                ('current_use_count', models.PositiveIntegerField(default=0)),
                ('total_use_count', models.PositiveIntegerField(default=0)),
                ('current_use_max', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]