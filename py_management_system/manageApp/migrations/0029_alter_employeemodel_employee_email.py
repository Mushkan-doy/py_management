# Generated by Django 4.1.3 on 2022-12-28 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0028_alter_salarymodel_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemodel',
            name='employee_email',
            field=models.EmailField(max_length=100),
        ),
    ]
