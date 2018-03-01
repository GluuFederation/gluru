# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alert_name', models.CharField(max_length=100, choices=[(b'EMAIL_TICKET_SUBJECT', 'New ticket subject'), (b'EMAIL_TICKET_BODY', 'New ticket body'), (b'EMAIL_PROFILE_SUBJECT', 'New user subject'), (b'EMAIL_PROFILE_BODY', 'New user body'), (b'EMAIL_ANSwER_SUBJECT', 'New answer subject'), (b'EMAIL_ANSWER_BODY', 'New answer body'), (b'EMAIL_EDIT_SUBJECT', 'Tickets edit subject'), (b'EMAIL_EDIT_BODY', 'Tickets edit body'), (b'EMAIL_OLD_SUBJECT', 'Tickets remember subject'), (b'EMAIL_OLD_BODY', 'Tickets remember body'), (b'EMAIL_ANSWER_COPY_SUBJECT', 'Tickets answer copy subject'), (b'EMAIL_ANSWER_COPY_BODY', 'Tickets answer copy body'), (b'EMAIL_TICKET_COPY_SUBJECT', 'Ticket copy subject'), (b'EMAIL_TICKET_COPY_BODY', 'Ticket copy body'), (b'EMAIL_TICKET_ASSIGNED_SUBJECT', 'Ticket assigned subject'), (b'EMAIL_TICKET_ASSIGNED_BODY', 'Ticket assigned body')])),
                ('alert_template', models.TextField(max_length=5000)),
                ('alert_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('alert_order',),
                'verbose_name': 'Alert',
                'verbose_name_plural': 'Alertss',
            },
        ),
        migrations.CreateModel(
            name='AlertOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_email', models.CharField(default=b'', help_text='From email', max_length=100, verbose_name='From email')),
                ('email_host', models.CharField(default=b'', help_text='Email host', max_length=100, verbose_name='Email host')),
                ('host_user', models.CharField(default=b'', help_text='Email host user', max_length=100, verbose_name='Email host user')),
                ('host_pass', models.CharField(default=b'', help_text='Host password', max_length=100, verbose_name='Host password')),
                ('port', models.CharField(default=b'', help_text='Port', max_length=100, verbose_name='Port')),
                ('use_tls', models.BooleanField(default=False, help_text='Use TLS', verbose_name='Use TLS?')),
                ('send_alerts', models.BooleanField(default=False, help_text='Send alerts?', verbose_name='Send alerts?')),
                ('send_create_alerts', models.BooleanField(default=False, help_text='Send create alerts?', verbose_name='Send create alerts?')),
                ('send_edit_alerts', models.BooleanField(default=False, help_text='Send edit alerts?', verbose_name='Send edit alerts?')),
                ('send_response_alerts', models.BooleanField(default=False, help_text='Send response alerts?', verbose_name='Send response alerts?')),
                ('send_registred_alerts', models.BooleanField(default=False, help_text='Send registred alerts?', verbose_name='Send registred alerts?')),
                ('send_old_ticket_alerts', models.BooleanField(default=False, help_text='Send old ticket alerts?', verbose_name='Send old ticket alerts?')),
            ],
            options={
                'verbose_name': 'alerts options',
                'verbose_name_plural': 'alerts options',
            },
        ),
    ]
