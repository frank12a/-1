# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_foruser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='question_foruser.Questionnaire'),
        ),
    ]
