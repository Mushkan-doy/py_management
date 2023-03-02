# Generated by Django 4.1.3 on 2022-12-27 08:59

import django.core.validators
from django.db import migrations, models
import manageApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0027_alter_salarymodel_month_alter_salarymodel_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarymodel',
            name='year',
            field=models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), manageApp.models.SalaryModel.max_value_current_year]),
        ),
    ]
