# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='crm_type',
            field=models.CharField(default=b'user', max_length=30, choices=[(b'', b'---------'), (b'staff', b'Staff'), (b'manager', b'Manager'), (b'admin', b'Admin'), (b'named', b'Named'), (b'user', b'User')]),
        ),
    ]
