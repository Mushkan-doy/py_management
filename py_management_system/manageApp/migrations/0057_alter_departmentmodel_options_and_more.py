# Generated by Django 4.1.3 on 2023-01-12 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0056_alter_invoicemodel_per_hrs_rate_dollar_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentmodel',
            options={'verbose_name': 'Department Model'},
        ),
        migrations.AlterModelOptions(
            name='employeemodel',
            options={'verbose_name': 'Employee Model'},
        ),
        migrations.AlterModelOptions(
            name='employeetypemodel',
            options={'verbose_name': 'EmployeeType Model'},
        ),
        migrations.AlterModelOptions(
            name='invoicemodel',
            options={'verbose_name': 'Invoice Model'},
        ),
        migrations.AlterModelOptions(
            name='pmsummarymodel',
            options={'verbose_name': 'PMSummary Model'},
        ),
        migrations.AlterModelOptions(
            name='projectmodel',
            options={'verbose_name': 'Project Model'},
        ),
        migrations.AlterModelOptions(
            name='salarymodel',
            options={'verbose_name': 'Salary Model'},
        ),
        migrations.AlterModelOptions(
            name='summarymodel',
            options={'verbose_name': 'Summary Model'},
        ),
    ]
