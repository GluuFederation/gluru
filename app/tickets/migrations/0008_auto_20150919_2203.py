# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_document_viewed_no'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='ticket',
        #     name='category',
        #     field=models.ForeignKey(related_name='category_tickets', verbose_name='Category', to='categories.Category', help_text='Ticket category'),
        # ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', help_text='Ticket priority', max_length=100, verbose_name='Priority', choices=[(b'', b'---------'), (b'P2', 'Medium'), (b'P0', 'Community'), (b'P1', 'High'), (b'P3', 'Low')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', help_text='Ticket status', max_length=100, verbose_name='Status', choices=[(b'', b'---------'), (b'Assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'Closed', 'Closed'), (b'New', 'New'), (b'InProgress', 'In Progress'), (b'Expired', 'Expired'), (b'Rejected', 'Rejected'), (b'Pending Input', 'Pending Input')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=b'product', choices=[(b'', b'---------'), (b'Administration', 'Administration'), (b'Product', 'Product'), (b'User', 'User')], max_length=255, blank=True, help_text='Ticket type', verbose_name='Type'),
        ),
    ]
