# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-11 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170611_1203'),
        ('events', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='p_person',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='post',
            name='p_sub_category',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.SubCategory'),
        ),
    ]
