# Generated by Django 4.1.3 on 2022-12-29 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0031_alter_employeemodel_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employeemodel',
            unique_together={('employee_email',)},
        ),
    ]