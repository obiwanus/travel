# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('comment', models.TextField(default='')),
            ],
        ),
    ]