# Generated by Django 4.1.3 on 2022-12-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0041_alter_projectmodel_project_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='expected_hrs',
            field=models.CharField(default='00:00', max_length=255),
        ),
    ]