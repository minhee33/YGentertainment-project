# Generated by Django 3.2.10 on 2022-02-09 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='execute_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period',
            field=models.TimeField(null=True),
        ),
    ]