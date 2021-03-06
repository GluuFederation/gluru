# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-08 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0019_auto_20160808_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.CharField(blank=True, default=b'', help_text=b'Company info added by user upon registration', max_length=255),
        ),
        migrations.AddField(
            model_name='partnership',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='profiles.Company'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='profiles.Company'),
        ),
        migrations.AlterUniqueTogether(
            name='partnership',
            unique_together=set([('client', 'partner')]),
        ),
    ]
