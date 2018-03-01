# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0021_auto_20151119_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='SugarCrmConnectors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sugarcrm_id', models.CharField(default=b'', max_length=50, null=True, verbose_name='CRM id', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('answer', models.ForeignKey(related_name='answer_sugarcrm_id', blank=True, to='tickets.Answer', null=True)),
                ('profile', models.ForeignKey(related_name='profile_sugarcrm_id', blank=True, to='tickets.Ticket', null=True)),
                ('ticket', models.ForeignKey(related_name='ticket_sugarcrm_id', blank=True, to='tickets.Ticket', null=True)),
            ],
            options={
                'ordering': ('added',),
                'verbose_name': 'SugarCRM',
                'verbose_name_plural': 'SugarCRM',
            },
        ),
    ]
