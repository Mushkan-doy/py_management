# Generated by Django 4.1.3 on 2023-01-12 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0048_alter_projectmodel_project_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='project_end_date',
            field=models.DateField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='projectmodel',
            name='project_start_date',
            field=models.DateField(default='', null=True),
        ),
    ]
