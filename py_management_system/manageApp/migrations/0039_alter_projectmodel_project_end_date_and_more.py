# Generated by Django 4.1.3 on 2022-12-30 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0038_alter_projectmodel_project_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='project_end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='projectmodel',
            name='project_start_date',
            field=models.DateField(),
        ),
    ]
