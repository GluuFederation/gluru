# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        # ('categories', '0001_initial'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['date_added'], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='added',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='modified',
            new_name='date_modified',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='deleted',
            new_name='is_deleted',
        ),
        # migrations.AddField(
        #     model_name='ticket',
        #     name='category',
        #     field=models.ForeignKey(related_name='ticket_category', to='categories.Category'),
        #     preserve_default=False,
        # ),
        migrations.AddField(
            model_name='ticket',
            name='date_due',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='etc',
            field=models.CharField(default=b'medium', max_length=255, blank=True, choices=[(b'medium', 'Medium'), (b'long', 'Long'), (b'short', 'Short')]),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='link_url',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='viewed_no',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
