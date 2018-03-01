# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0004_auto_20150902_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.CharField(max_length=100, blank=True)),
                ('data_type', models.CharField(max_length=100, blank=True)),
                ('before_value_string', models.CharField(max_length=255, blank=True)),
                ('after_value_string', models.CharField(max_length=255, blank=True)),
                ('before_value_text', models.TextField(blank=True)),
                ('after_value_text', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('crm_id', uuidfield.fields.UUIDField(max_length=32, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='ticket_modified_by', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(related_name='ticket_history', to='tickets.Ticket')),
            ],
            options={
                'ordering': ['date_added'],
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
    ]
