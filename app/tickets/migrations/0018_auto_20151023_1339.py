# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_auto_20151023_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketdocuments',
            old_name='name',
            new_name='file',
        ),
    ]
