# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-11 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_auth', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.SmallIntegerField(choices=[(0, 'Normal user'), (1, 'User manager'), (2, 'Administrator')], default=0),
        ),
    ]
