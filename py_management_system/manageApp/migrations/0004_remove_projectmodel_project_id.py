# Generated by Django 4.1.3 on 2022-12-05 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0003_employeetypemodel_alter_employeemodel_employee_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodel',
            name='project_id',
        ),
    ]
