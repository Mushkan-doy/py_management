# Generated by Django 4.1.3 on 2022-12-06 12:02

import django.core.validators
from django.db import migrations, models
import manageApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0006_rename_employee_salarymodel_bde_name'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='departmentheadcountsummarymodel',
        #     name='month',
        #     field=models.CharField(max_length=100),
        # ),
        # migrations.AlterField(
        #     model_name='departmentheadcountsummarymodel',
        #     name='year',
        #     field=models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), manageApp.models.DepartmentHeadcountSummaryModel.max_value_current_year]),
        # ),
        migrations.AlterField(
            model_name='employeemodel',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='relieving_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salarymodel',
            name='month',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='salarymodel',
            name='salary',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salarymodel',
            name='year',
            field=models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), manageApp.models.SalaryModel.max_value_current_year]),
        ),
    ]
