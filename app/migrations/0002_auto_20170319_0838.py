# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 15:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callrequest',
            name='completed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completed_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
