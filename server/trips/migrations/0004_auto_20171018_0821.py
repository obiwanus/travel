# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_auto_20171015_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
    ]
