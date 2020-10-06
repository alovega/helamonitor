# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-02 15:17
from __future__ import unicode_literals

import api.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.App')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=255)),
                ('expires_at', models.DateTimeField(default=api.models.token_expiry)),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppUser')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
