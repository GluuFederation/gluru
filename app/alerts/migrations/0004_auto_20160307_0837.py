# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_auto_20160106_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to', models.CharField(max_length=100, verbose_name='To')),
                ('email', models.TextField(max_length=5000, verbose_name='Email')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
            ],
            options={
                'verbose_name': 'email sent',
                'verbose_name_plural': 'emails sent',
            },
        ),
        migrations.AlterField(
            model_name='alert',
            name='alert_name',
            field=models.CharField(max_length=100, choices=[(b'EMAIL_TICKET_SUBJECT_BY_STAFF', 'New ticket subject(added by staff)'), (b'EMAIL_TICKET_SUBJECT', 'New ticket subject'), (b'EMAIL_TICKET_BODY', 'New ticket body'), (b'EMAIL_PROFILE_SUBJECT', 'New user subject'), (b'EMAIL_PROFILE_BODY', 'New user body'), (b'EMAIL_ANSwER_SUBJECT', 'New answer subject'), (b'EMAIL_ANSWER_BODY', 'New answer body'), (b'EMAIL_EDIT_SUBJECT', 'Tickets edit subject'), (b'EMAIL_EDIT_BODY', 'Tickets edit body'), (b'EMAIL_OLD_SUBJECT', 'Tickets remember subject'), (b'EMAIL_OLD_BODY', 'Tickets remember body'), (b'EMAIL_ANSWER_COPY_SUBJECT', 'Tickets answer copy subject'), (b'EMAIL_ANSWER_COPY_BODY', 'Tickets answer copy body'), (b'EMAIL_TICKET_COPY_SUBJECT', 'Ticket copy subject'), (b'EMAIL_TICKET_COPY_BODY', 'Ticket copy body'), (b'EMAIL_TICKET_ASSIGNED_SUBJECT', 'Ticket assigned subject'), (b'EMAIL_TICKET_ASSIGNED_BODY', 'Ticket assigned body'), (b'EMAIL_CREATOR_TICKET_ASSIGNED_SUBJECT', 'Ticket assigned subject - for creator'), (b'EMAIL_CREATOR_TICKET_ASSIGNED_BODY', 'Ticket assigned body - for creator')]),
        ),
    ]
