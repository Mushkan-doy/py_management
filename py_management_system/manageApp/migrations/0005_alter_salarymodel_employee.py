# Generated by Django 4.1.3 on 2022-12-06 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0004_remove_projectmodel_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarymodel',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageApp.employeemodel', verbose_name='bde_name'),
        ),
    ]
