# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0015_auto_20151022_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.FileField(max_length=255, upload_to=tickets.models.ticket_file_path, blank=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='The document has been deleted?', verbose_name='Deleted')),
                ('viewed_no', models.IntegerField(default=0, help_text='Document number of views', verbose_name='Viewed', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['date_added'],
                'verbose_name': 'ticket document',
                'verbose_name_plural': 'ticket documents',
            },
        ),
        migrations.RemoveField(
            model_name='document',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='document',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='document',
            name='user',
        ),
        migrations.AddField(
            model_name='answer',
            name='file',
            field=models.FileField(max_length=255, upload_to='', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', max_length=100, verbose_name='Priority', choices=[(b'', b'Choose ticket priority'), (b'medium', 'Medium'), (b'community', 'Community'), (b'high', 'High'), (b'low', 'Low')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', max_length=100, verbose_name='Status', choices=[(b'', b'Choose ticket status'), (b'assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'closed', 'Closed'), (b'new', 'New'), (b'inprogress', 'In Progress'), (b'expired', 'Expired'), (b'rejected', 'Rejected'), (b'pending', 'Pending Input')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=b'product', max_length=255, verbose_name='Type', blank=True, choices=[(b'', b'Choose ticket type'), (b'admin', 'Administration'), (b'product', 'Product'), (b'user', 'User')]),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AddField(
            model_name='ticketdocuments',
            name='ticket',
            field=models.ForeignKey(related_name='ticket_document', blank=True, to='tickets.Ticket', null=True),
        ),
        migrations.AddField(
            model_name='ticketdocuments',
            name='user',
            field=models.ForeignKey(related_name='document_added_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
