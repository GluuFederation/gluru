# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0002_auto_20150902_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', help_text='Answer title', max_length=255, verbose_name='Title')),
                ('description', models.TextField(default=b'', help_text='Answer description', verbose_name='Description')),
                ('link_url', models.CharField(default=b'', help_text='Video or sceenshot url', max_length=255, verbose_name='Link URL', blank=True)),
                ('privacy', models.CharField(default=b'inherit', choices=[(b'inherit', 'Inherit'), (b'public', 'Public'), (b'private', 'Private')], max_length=255, blank=True, help_text='Answer privacy', verbose_name='Privacy')),
                ('is_deleted', models.BooleanField(default=False, help_text='The answer is deleted?', verbose_name='Deleted')),
                ('is_viewed', models.BooleanField(default=False, help_text='The answer has been seen?', verbose_name='Viewed')),
                ('date_added', models.DateTimeField(help_text='Added date', verbose_name='Added', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text='Modified date', verbose_name='Modified', auto_now=True)),
                ('crm_id', uuidfield.fields.UUIDField(max_length=32, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='answer_created_by', verbose_name='Created by', to=settings.AUTH_USER_MODEL, help_text='Answer added by user')),
                ('ticket', models.ForeignKey(related_name='ticket_answers', verbose_name='Ticket', to='tickets.Ticket', help_text='Ticket')),
            ],
            options={
                'ordering': ['date_added'],
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assigned_to',
            field=models.ForeignKey(related_name='ticket_assigned_to', blank=True, to=settings.AUTH_USER_MODEL, help_text='Ticket assigned to user', null=True, verbose_name='Assigned to'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(related_name='ticket_created_by', verbose_name='Created by', to=settings.AUTH_USER_MODEL, help_text='Ticket created by user'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_added',
            field=models.DateTimeField(help_text='Added date', verbose_name='Added', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_due',
            field=models.DateTimeField(help_text='Ticked completion date', null=True, verbose_name='Due date', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_modified',
            field=models.DateTimeField(help_text='Modified date', verbose_name='Modified', auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_start',
            field=models.DateTimeField(help_text='Ticket start date', null=True, verbose_name='Start date', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(default=b'', help_text='Ticket description', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='etc',
            field=models.CharField(default=b'', choices=[(b'medium', 'Medium'), (b'long', 'Long'), (b'short', 'Short')], max_length=255, blank=True, help_text='Ticket estimate time of completion', verbose_name='Etc'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='The ticket is deleted?', verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_private',
            field=models.BooleanField(default=False, help_text='The ticket is private?', verbose_name='Private'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='is_viewed',
            field=models.BooleanField(default=False, help_text='The ticket has been seen?', verbose_name='Viewed'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='link_url',
            field=models.CharField(default=b'', help_text='Video or sceenshot url', max_length=255, verbose_name='Link URL', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', help_text='Ticket priority', max_length=100, verbose_name='Priority', choices=[(b'', b'---------'), (b'medium', 'Medium'), (b'community', 'Community'), (b'hight', 'High'), (b'low', 'Low')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', help_text='Ticket status', max_length=100, verbose_name='Status', choices=[(b'', b'---------'), (b'assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'closed', 'Closed'), (b'new', 'New'), (b'progress', 'In Progress'), (b'expired', 'Expired'), (b'rejected', 'Rejected'), (b'pending', 'Pending Input')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(default=b'', help_text='Ticket title', max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=b'product', choices=[(b'', b'---------'), (b'administration', 'Administration'), (b'product', 'Product'), (b'user', 'User')], max_length=255, blank=True, help_text='Ticket type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='viewed_no',
            field=models.IntegerField(default=0, help_text='Ticket number of views', verbose_name='Viewed', blank=True),
        ),
    ]
