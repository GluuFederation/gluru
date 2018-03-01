# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0024_auto_20160101_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='etc',
            field=models.CharField(default=b'', max_length=255, verbose_name='ETC', blank=True, choices=[(b'', b'How long will it take to resolve this ticket?'), (b'medium', 'Medium'), (b'long', 'Long'), (b'short', 'Short')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', max_length=100, verbose_name='Status', choices=[(b'', b'Choose ticket status'), (b'assigned', 'Assigned'), (b'closed', 'Closed'), (b'new', 'New'), (b'inprogress', 'In Progress'), (b'expired', 'Expired'), (b'rejected', 'Rejected'), (b'pending', 'Pending Input')]),
        ),
    ]
