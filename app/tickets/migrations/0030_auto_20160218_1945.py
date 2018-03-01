# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0029_auto_20160207_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketalerts',
            name='user',
            field=models.ForeignKey(related_name='user_alerts', default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
