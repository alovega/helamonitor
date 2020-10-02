# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-02 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='app',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State'),
        ),
        migrations.AddField(
            model_name='app',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
    ]