# Generated by Django 2.1 on 2018-08-09 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotficationContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Contact name', max_length=100)),
                ('number', models.CharField(help_text='Contact Number', max_length=100)),
                ('priority', models.CharField(choices=[('H', 'High'), ('L', 'Low')], default='H', help_text='Priority', max_length=1)),
                ('enabled', models.BooleanField(default=True, verbose_name='Is Enabled?')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='TicketNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(help_text='User associated with this ticket notification', max_length=20)),
                ('is_subscribed', models.BooleanField(default=True, help_text='Indicate whether user subscribe to notification')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to='tickets.Ticket')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='ticketnotification',
            unique_together={('ticket', 'user')},
        ),
    ]