# Generated by Django 3.2.10 on 2022-01-17 13:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20220117_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialbladeyoutube',
            name='reserved_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
