# Generated by Django 4.1.3 on 2022-12-19 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0017_alter_projectmodel_project_end_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DepartmentHeadcountSummaryModel',
        ),
    ]