# Generated by Django 4.1.3 on 2022-12-30 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0036_employeemodel_comments_projectmodel_comments_and_more'),
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