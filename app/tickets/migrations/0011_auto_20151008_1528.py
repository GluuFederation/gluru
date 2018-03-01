# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_auto_20151008_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='answers_no',
            field=models.IntegerField(default=0, verbose_name='Answers number', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assigned_to',
            field=models.ForeignKey(related_name='ticket_assigned_to', verbose_name='Assigned to', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(related_name='ticket_created_by', verbose_name='Created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Added'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_start',
            field=models.DateTimeField(null=True, verbose_name='Start date', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='due_date',
            field=models.DateTimeField(null=True, verbose_name='Due date', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='etc',
            field=models.CharField(default=b'', max_length=255, verbose_name='Etc', blank=True, choices=[(b'medium', 'Medium'), (b'long', 'Long'), (b'short', 'Short')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Private'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_viewed',
            field=models.BooleanField(default=False, verbose_name='Viewed'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='link_url',
            field=models.CharField(default=b'', max_length=255, verbose_name='Link URL', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', max_length=100, verbose_name='Priority', choices=[(b'', b'---------'), (b'P2', 'Medium'), (b'P0', 'Community'), (b'P1', 'High'), (b'P3', 'Low')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='send_copy',
            field=models.CharField(default=b'', max_length=255, verbose_name='Copy addr', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', max_length=100, verbose_name='Status', choices=[(b'', b'---------'), (b'Assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'Closed', 'Closed'), (b'New', 'New'), (b'InProgress', 'In Progress'), (b'Expired', 'Expired'), (b'Rejected', 'Rejected'), (b'Pending Input', 'Pending Input')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=b'product', max_length=255, verbose_name='Type', blank=True, choices=[(b'', b'---------'), (b'Administration', 'Administration'), (b'Product', 'Product'), (b'User', 'User')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='viewed_no',
            field=models.IntegerField(default=0, verbose_name='Viewed', blank=True),
        ),
    ]
