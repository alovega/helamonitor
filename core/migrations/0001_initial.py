# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-02 15:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('username',),
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=250)),
                ('optimal_response_time', models.DurationField(default=datetime.timedelta(0, 3))),
                ('endpoint_type', models.ForeignKey(help_text='Endpoint type e.g an health-check endpoint', on_delete=django.db.models.deletion.CASCADE, to='base.EndpointType')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EscalationRule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('nth_event', models.IntegerField(default=1, help_text='Limit of n events to satisfy this rule')),
                ('duration', models.DurationField(blank=True, help_text='Time period within which the nth occurrence of an event type will be escalated', null=True)),
                ('escalation_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EscalationLevel')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EventType')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(help_text='Method where the error is origination from', max_length=100, null=True)),
                ('request', models.TextField(blank=True, max_length=1000, null=True)),
                ('response', models.TextField(blank=True, max_length=1000, null=True)),
                ('stack_trace', models.TextField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, help_text='Informative description of the event', max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EventType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('priority_level', models.IntegerField(default=1)),
                ('scheduled_for', models.DateTimeField(blank=True, help_text='Time the scheduled maintenance should begin', null=True)),
                ('scheduled_until', models.DateTimeField(blank=True, help_text='Time the scheduled maintenance should end', null=True)),
                ('event_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.EventType')),
                ('incident_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.IncidentType')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IncidentEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Event')),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Incident')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IncidentLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('priority_level', models.IntegerField()),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('escalation_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EscalationLevel')),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Incident')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.CharField(max_length=255)),
                ('message', models.TextField(max_length=255)),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.NotificationType')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(default='1.0.0', max_length=10)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SystemCredential',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(help_text='Similar to a client_ID', max_length=100)),
                ('password', models.CharField(help_text='Similar to a client_Secret', max_length=100)),
                ('token', models.CharField(help_text='Authorization token', max_length=100)),
                ('expires_at', models.DateTimeField(blank=True, help_text='Expiry time of the authorization token', null=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SystemMonitor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('response_time', models.DurationField(blank=True, default=datetime.timedelta(0), null=True)),
                ('response_time_speed', models.CharField(blank=True, choices=[('Slow', 'Slow'), ('Normal', 'Normal')], default='Normal', max_length=100, null=True)),
                ('response_body', models.CharField(blank=True, help_text='Body of the response returned when querying an endpoint', max_length=100, null=True)),
                ('response_code', models.PositiveIntegerField(blank=True, null=True)),
                ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Endpoint')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SystemRecipient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('escalation_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EscalationLevel')),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.NotificationType')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AddField(
            model_name='interface',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AddField(
            model_name='incident',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AddField(
            model_name='event',
            name='interface',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Interface'),
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.State'),
        ),
        migrations.AddField(
            model_name='event',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AddField(
            model_name='escalationrule',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.System'),
        ),
        migrations.AlterUniqueTogether(
            name='system',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('username',)]),
        ),
    ]
