# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-23 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0003_auto_20171123_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='upvotes',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_name', to='qna.Question'),
        ),
    ]
