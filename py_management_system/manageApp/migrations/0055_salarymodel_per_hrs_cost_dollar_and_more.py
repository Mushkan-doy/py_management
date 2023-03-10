# Generated by Django 4.1.3 on 2023-01-12 07:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import manageApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0054_alter_salarymodel_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarymodel',
            name='per_hrs_cost_dollar',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='salarymodel',
            name='per_hrs_cost_inr',
            field=models.FloatField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='joining_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Probation'), ('2', 'Confirmed'), ('3', 'Notice'), ('4', 'Terminate'), ('5', 'Relieve')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='salarymodel',
            name='salary',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.CreateModel(
            name='InvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(default=None, max_length=100)),
                ('year', models.PositiveIntegerField(default=2023, validators=[django.core.validators.MinValueValidator(1984), manageApp.models.InvoiceModel.max_value_current_year])),
                ('invoice_amount', models.FloatField()),
                ('per_hrs_rate_inr', models.FloatField(blank=True, default='0')),
                ('per_hrs_rate_dollar', models.IntegerField(blank=True, default='0')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.projectmodel')),
            ],
            options={
                'db_table': 'invoice_master',
            },
        ),
    ]
