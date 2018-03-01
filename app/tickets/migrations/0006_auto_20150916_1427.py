# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0005_tickethistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.FileField(max_length=255, upload_to=tickets.models.ticket_file_path, blank=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='The document has been deleted?', verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('answer', models.ForeignKey(related_name='answer_document', blank=True, to='tickets.Answer', null=True)),
                ('ticket', models.ForeignKey(related_name='ticket_document', blank=True, to='tickets.Ticket', null=True)),
                ('user', models.ForeignKey(related_name='document_added_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added'],
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.AlterModelOptions(
            name='tickethistory',
            options={'ordering': ['date_added'], 'verbose_name': 'ticket history', 'verbose_name_plural': 'tickets history'},
        ),
    ]
