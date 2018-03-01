# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0026_auto_20160108_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='modified_by',
            field=models.ForeignKey(related_name='ticket_modified_by', default='', verbose_name='Modified by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
