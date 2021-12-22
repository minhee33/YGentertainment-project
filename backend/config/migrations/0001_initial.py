# Generated by Django 3.2.10 on 2021-12-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.TextField(default='login')),
                ('user_id', models.TextField(null=True)),
                ('user_pw', models.TextField(null=True)),
                ('api_key', models.TextField(null=True)),
                ('secret_key', models.TextField(null=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'auth_info',
            },
        ),
        migrations.CreateModel(
            name='CollectTargetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_name', models.TextField(default='')),
                ('target_type', models.TextField(default='int')),
                ('xpath', models.TextField(default='')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'collect_target_item',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('url', models.TextField(unique=True)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'platform',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_type', models.TextField(default='')),
                ('excute_time', models.TimeField()),
                ('period', models.TextField(default='hour')),
                ('active', models.BooleanField(default=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
    ]
