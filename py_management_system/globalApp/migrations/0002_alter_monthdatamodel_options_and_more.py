# Generated by Django 4.1.3 on 2023-01-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthdatamodel',
            options={'verbose_name': 'MonthlyData Model'},
        ),
        migrations.AlterField(
            model_name='monthdatamodel',
            name='dollar_rate',
            field=models.FloatField(),
        ),
    ]
