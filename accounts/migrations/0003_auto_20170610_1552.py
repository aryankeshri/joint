# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-10 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default=None, max_length=250),
        ),
    ]
