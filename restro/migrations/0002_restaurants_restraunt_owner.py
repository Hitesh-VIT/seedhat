# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 21:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='restraunt_owner',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
