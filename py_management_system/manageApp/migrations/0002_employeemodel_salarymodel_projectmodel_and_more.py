# Generated by Django 4.1.3 on 2022-12-05 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=255)),
                ('employee_email', models.EmailField(max_length=100, unique=True)),
                ('joining_date', models.DateField()),
                ('relieving_date', models.DateField()),
                ('employee_type', models.CharField(max_length=30)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.departmentmodel')),
            ],
            options={
                'db_table': 'employee_master',
            },
        ),
        migrations.CreateModel(
            name='SalaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateTimeField()),
                ('year', models.DateTimeField()),
                ('salary', models.FloatField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.employeemodel')),
            ],
            options={
                'db_table': 'salary_master',
            },
        ),
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=100, unique=True)),
                ('project_name', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=255)),
                ('project_start_date', models.DateField()),
                ('project_end_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.employeemodel')),
            ],
            options={
                'db_table': 'project_master',
            },
        ),
        migrations.CreateModel(
            name='ProjectDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateTimeField()),
                ('year', models.DateTimeField()),
                ('total_freeze_hrs', models.DateTimeField()),
                ('total_billable_hrs', models.DateTimeField()),
                ('no_of_resources', models.IntegerField()),
                ('developer_hrs', models.DateTimeField()),
                ('designer_hrs', models.DateTimeField()),
                ('qa_hrs', models.DateTimeField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.employeemodel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.projectmodel')),
            ],
            options={
                'db_table': 'project_data_master',
            },
        ),
        migrations.CreateModel(
            name='DepartmentHeadcountSummaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateTimeField()),
                ('year', models.DateTimeField()),
                ('total_count', models.CharField(max_length=100)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.departmentmodel')),
            ],
            options={
                'db_table': 'department_headcount_summary_master',
            },
        ),
    ]
