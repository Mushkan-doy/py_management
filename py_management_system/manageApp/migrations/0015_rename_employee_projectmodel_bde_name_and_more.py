# Generated by Django 4.1.3 on 2022-12-13 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0014_rename_employee_projectdatamodel_pm_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectmodel',
            old_name='employee',
            new_name='bde_name',
        ),
        migrations.RenameField(
            model_name='salarymodel',
            old_name='bde_name',
            new_name='employee',
        ),
    ]
