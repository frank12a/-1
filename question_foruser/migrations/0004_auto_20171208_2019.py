# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 12:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_foruser', '0003_auto_20171206_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question_foruser.Option'),
        ),
    ]
