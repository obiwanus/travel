# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 02:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_auth', '0004_user'),
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='travel_auth.User'),
            preserve_default=False,
        ),
    ]