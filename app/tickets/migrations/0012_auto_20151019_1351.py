# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0011_auto_20151008_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketAlerts',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date_added'],
                'verbose_name': 'alert',
                'verbose_name_plural': 'alerts',
            },
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(default=b'', help_text='This field supports markdown language.                             <a target="_blank" href="http://dillinger.io/">Information here</a>', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='due_date',
            field=models.DateField(null=True, verbose_name='Due date', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='etc',
            field=models.CharField(default=b'', max_length=255, verbose_name='ETC', blank=True, choices=[(b'', b'Choose an estimate time to complate'), (b'medium', 'Medium'), (b'long', 'Long'), (b'short', 'Short')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', max_length=100, verbose_name='Priority', choices=[(b'', b'Choose ticket priority'), (b'P2', 'Medium'), (b'P0', 'Community'), (b'P1', 'High'), (b'P3', 'Low')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='send_copy',
            field=models.CharField(default=b'', max_length=255, verbose_name='Send copy to', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=b'new', max_length=100, verbose_name='Status', choices=[(b'', b'Choose ticket status'), (b'Assigned', 'Assigned'), (b'inherit', 'Inherit'), (b'Closed', 'Closed'), (b'New', 'New'), (b'InProgress', 'In Progress'), (b'Expired', 'Expired'), (b'Rejected', 'Rejected'), (b'Pending Input', 'Pending Input')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(default=b'', max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=b'product', max_length=255, verbose_name='Type', blank=True, choices=[(b'', b'Choose ticket type'), (b'Administration', 'Administration'), (b'Product', 'Product'), (b'User', 'User')]),
        ),
        migrations.AddField(
            model_name='ticketalerts',
            name='ticket',
            field=models.ForeignKey(related_name='ticket_alerts', to='tickets.Ticket'),
        ),
        migrations.AddField(
            model_name='ticketalerts',
            name='user',
            field=models.ForeignKey(related_name='user_alerts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='ticketalerts',
            unique_together=set([('ticket', 'user')]),
        ),
    ]
