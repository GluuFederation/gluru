# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0078_auto_20170622_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='product',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name='Product Version', choices=[(b'', b'Select a Product'), (b'GLUU', b'Gluu Server'), (b'OXD', b'OXD'), (b'SUP_GLUU', b'Super Gluu'), (b'CLUSTER', b'Cluster Manager')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='product_version',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name='Product Version', choices=[(b'', b'Select a Product Version'), (b'3.0.2', b'3.0.2'), (b'3.0.1', b'3.0.1'), (b'2.4.4.3', b'2.4.4.3'), (b'2.4.4.2', b'2.4.4.2'), (b'2.4.4', b'2.4.4'), (b'2.4.3', b'2.4.3'), (b'2.4.2', b'2.4.2'), (b'1.0', b'1.0'), (b'Other', b'Other')]),
        ),
    ]
