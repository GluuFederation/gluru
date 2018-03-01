# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0076_auto_20170622_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_category',
            field=models.CharField(max_length=20, verbose_name='Category', choices=[(b'', b'Select a Category'), (b'OUTAGE', b'Outages'), (b'IDNTY', b'Identity Management'), (b'SSO', b'Single Sign-On'), (b'MFA', b'Authentication'), (b'ACCESS', b'Access Management'), (b'CUSTOM', b'Customization'), (b'FEATURE', b'Feature Request'), (b'INSTALLATION', b'Installation'), (b'UPGRADE', b'Upgrade'), (b'MAINTENANCE', b'Maintenance'), (b'OTHER', b'Other')]),
        ),
    ]
