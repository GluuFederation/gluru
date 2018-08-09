# Generated by Django 2.1 on 2018-08-09 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_by', models.CharField(help_text='Answer added by user', max_length=20)),
                ('link_url', models.URLField(blank=True, max_length=255, verbose_name='Link URL')),
                ('privacy', models.CharField(blank=True, choices=[('', '---------'), ('IH', 'Inherit'), ('PU', 'Public'), ('PR', 'Private')], max_length=2)),
                ('send_copy', models.CharField(blank=True, default='', max_length=255, verbose_name='Send copy to')),
                ('is_deleted', models.BooleanField(blank=True, default=False, help_text='The answer is deleted?', verbose_name='Deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('category', models.CharField(choices=[('IN', 'Installation'), ('OA', 'Outages'), ('SO', 'Single Sign-On'), ('AU', 'Authentication'), ('AZ', 'Authorization'), ('AM', 'Access Management'), ('UG', 'Upgrade'), ('MT', 'Maintenance'), ('IM', 'Identity Management'), ('CZ', 'Customization'), ('FR', 'Feature Request'), ('LO', 'Logout'), ('OH', 'Other')], default='IN', max_length=2, verbose_name='Category')),
                ('created_by', models.CharField(max_length=20)),
                ('created_for', models.CharField(blank=True, max_length=20, null=True)),
                ('company', models.CharField(blank=True, max_length=20, null=True, verbose_name='Company Association')),
                ('updated_by', models.CharField(blank=True, max_length=20, null=True, verbose_name='Last Updated by')),
                ('assignee', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('', 'Select a Status'), ('NW', 'New'), ('AS', 'Assigned'), ('IP', 'In Progress'), ('PI', 'Pending Input'), ('CL', 'Closed')], default='NW', max_length=2)),
                ('issue_type', models.CharField(choices=[('', 'Please specify the kind of issue you have encountered'), ('PO', 'Production Outage'), ('PI', 'Production Impaired'), ('PP', 'Pre-Production Issue'), ('MI', 'Minor Issue'), ('NI', 'New Development Issue')], default='', max_length=2)),
                ('server_version', models.CharField(choices=[('', 'Select Gluu Server Version'), ('3.1.2', 'Gluu Server 3.1.2'), ('3.1.1', 'Gluu Server 3.1.1'), ('3.1.0', 'Gluu Server 3.1.0'), ('3.0.2', 'Gluu Server 3.0.2'), ('3.0.1', 'Gluu Server 3.0.1'), ('2.4.4.3', 'Gluu Server 2.4.4.3'), ('2.4.4.2', 'Gluu Server 2.4.4.2'), ('2.4.4', 'Gluu Server 2.4.4'), ('2.4.3', 'Gluu Server 2.4.3'), ('2.4.2', 'Gluu Server 2.4.2'), ('Other', 'Other')], default='', help_text='Gluu Server Version', max_length=10)),
                ('server_version_comments', models.CharField(blank=True, help_text='Gluu Server Version Comments', max_length=30, null=True)),
                ('os_version', models.CharField(choices=[('', 'Select Operating System'), ('UT', 'Ubuntu'), ('CO', 'CentOS'), ('RH', 'RHEL'), ('DB', 'Debian')], default='', help_text='Which OS are you using?', max_length=2, verbose_name='OS')),
                ('os_version_name', models.CharField(max_length=10, verbose_name='OS Version')),
                ('answers_no', models.IntegerField(blank=True, default=0, verbose_name='Answers number')),
                ('link', models.URLField(blank=True, max_length=255, verbose_name='Link URL')),
                ('send_copy', models.CharField(blank=True, max_length=255, verbose_name='Send copy to')),
                ('is_private', models.BooleanField(blank=True, default=False, verbose_name='Private')),
                ('is_deleted', models.BooleanField(blank=True, default=False, verbose_name='Deleted')),
                ('os_type', models.BooleanField(blank=True, default=False, help_text='Is it 64-bit hardware?')),
                ('ram', models.BooleanField(blank=True, default=False, help_text='Does the server have at least 4GB RAM?')),
                ('visits', models.IntegerField(blank=True, default=0, verbose_name='Ticket visits')),
                ('meta_keywords', models.CharField(blank=True, max_length=500, null=True)),
                ('set_default_gluu', models.BooleanField(blank=True, default=False, verbose_name='Default Gluu')),
                ('is_notified', models.BooleanField(default=False, help_text='Indicate this ticket would be notified to admin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, choices=[('', 'Select a Product'), ('OD', 'OXD'), ('SG', 'Super Gluu'), ('CM', 'Cluster Manager')], max_length=2)),
                ('version', models.CharField(blank=True, choices=[('', 'Select Product Version'), ('3.1.1', '3.1.1'), ('3.0.2', '3.0.2'), ('3.0.1', '3.0.1'), ('2.4.4.3', '2.4.4.3'), ('2.4.4.2', '2.4.4.2'), ('2.4.4', '2.4.4'), ('2.4.3', '2.4.3'), ('2.4.2', '2.4.2'), ('1.0', '1.0'), ('Alpha', 'Alpha'), ('Other', 'Other')], max_length=10, verbose_name='Product Version')),
                ('os_version', models.CharField(blank=True, choices=[('', 'Select Operating System'), ('UT', 'Ubuntu'), ('CO', 'CentOS'), ('RH', 'RHEL'), ('DB', 'Debian'), ('AD', 'Android'), ('IO', 'iOS'), ('BO', 'Both')], max_length=2, verbose_name='Product OS Version')),
                ('os_version_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Product OS Version')),
                ('ios_version_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='iOS Version')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='tickets.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tickets.Ticket'),
        ),
    ]
