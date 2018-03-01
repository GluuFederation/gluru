# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('type', models.CharField(default=b'user', max_length=255, blank=True, choices=[(b'', b'---------'), (b'administration', 'Administration'), (b'product', 'Product'), (b'user', 'User')])),
                ('status', models.CharField(default=b'new', max_length=100, blank=True, choices=[(b'', b'---------'), (b'assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'closed', 'Closed'), (b'new', 'New'), (b'progress', 'In Progress'), (b'expired', 'Expired'), (b'rejected', 'Rejected'), (b'pending', 'Pending Input')])),
                ('priority', models.CharField(default=b'low', max_length=100, blank=True, choices=[(b'', b'---------'), (b'medium', 'Medium'), (b'community', 'Community'), (b'hight', 'High'), (b'low', 'Low')])),
                ('deleted', models.BooleanField(default=0)),
                ('crm_id', uuidfield.fields.UUIDField(max_length=32, null=True, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(related_name='ticket_assigned_to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('created_by', models.ForeignKey(related_name='ticket_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['added'],
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]
