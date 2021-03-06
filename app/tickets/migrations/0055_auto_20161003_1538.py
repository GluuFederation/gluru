# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-03 15:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0054_auto_20160922_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketReminderBlacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.AlterField(
            model_name='ticket',
            name='issue_type',
            field=models.CharField(blank=True, choices=[(b'', 'Please specify the kind of issue you have encountered'), (b'outage', 'Production Outage'), (b'impaired', 'Production Impaired'), (b'pre_production', 'Pre-Production Issue'), (b'minor', 'Minor Issue'), (b'new_development', 'New Development Issue')], default=b'', max_length=20, verbose_name='Issue type'),
        ),
        migrations.AddField(
            model_name='ticketreminderblacklist',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to='tickets.Ticket'),
        ),
        migrations.AddField(
            model_name='ticketreminderblacklist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ticketreminderblacklist',
            unique_together=set([('ticket', 'user')]),
        ),
    ]
