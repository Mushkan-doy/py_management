# Generated by Django 4.1.3 on 2022-12-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0024_pmsummarymodel_submit_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summarymodel',
            name='existing_client_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
        migrations.AlterField(
            model_name='summarymodel',
            name='new_client_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
        migrations.AlterField(
            model_name='summarymodel',
            name='total_billable_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
        migrations.AlterField(
            model_name='summarymodel',
            name='total_expected_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
        migrations.AlterField(
            model_name='summarymodel',
            name='total_freeze_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
    ]
