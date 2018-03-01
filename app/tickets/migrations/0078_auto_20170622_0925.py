# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0077_auto_20170622_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='product',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name='Product Version'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='product_version',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name='Product Version', choices=[(b'', b'Select a Product'), (b'GLUU', b'Gluu Server'), (b'OXD', b'OXD'), (b'SUP_GLUU', b'Super Gluu'), (b'CLUSTER', b'Cluster Manager')]),
        ),
    ]
