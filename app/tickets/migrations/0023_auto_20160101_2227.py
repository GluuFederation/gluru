# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0022_ticket_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-date_added'], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AlterModelOptions(
            name='ticketalerts',
            options={'ordering': ['-date_added'], 'verbose_name': 'alert', 'verbose_name_plural': 'alerts'},
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_alerts',
            field=models.BooleanField(default=False, verbose_name='Send alerts?'),
        ),
    ]
