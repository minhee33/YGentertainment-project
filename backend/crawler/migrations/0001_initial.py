# Generated by Django 3.2.10 on 2022-01-21 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrowdtangleFacebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.BigIntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrowdtangleInstagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.BigIntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Melon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('listeners', models.BigIntegerField(null=True)),
                ('streams', models.BigIntegerField(null=True)),
                ('fans', models.IntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url1', models.TextField(null=True)),
                ('url2', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTiktok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField(null=True)),
                ('uploads', models.IntegerField(null=True)),
                ('likes', models.BigIntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTwitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField(null=True)),
                ('twits', models.IntegerField(null=True)),
                ('user_created', models.TextField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTwitter2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField(null=True)),
                ('twits', models.IntegerField(null=True)),
                ('user_created', models.TextField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeYoutube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('uploads', models.IntegerField(null=True)),
                ('subscribers', models.IntegerField(null=True)),
                ('views', models.BigIntegerField(null=True)),
                ('user_created', models.TextField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('monthly_listens', models.BigIntegerField(null=True)),
                ('followers', models.BigIntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url1', models.TextField(null=True)),
                ('url2', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vlive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('members', models.IntegerField(null=True)),
                ('videos', models.IntegerField(null=True)),
                ('likes', models.BigIntegerField(null=True)),
                ('plays', models.BigIntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weverse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('weverses', models.IntegerField(null=True)),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(null=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='weverse',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique weverse record'),
        ),
        migrations.AddConstraint(
            model_name='vlive',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique vlive record'),
        ),
        migrations.AddConstraint(
            model_name='spotify',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique spotify record'),
        ),
        migrations.AddConstraint(
            model_name='socialbladeyoutube',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique youtube record'),
        ),
        migrations.AddConstraint(
            model_name='socialbladetwitter2',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique twitter2 record'),
        ),
        migrations.AddConstraint(
            model_name='socialbladetwitter',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique twitter record'),
        ),
        migrations.AddConstraint(
            model_name='socialbladetiktok',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique tiktok record'),
        ),
        migrations.AddConstraint(
            model_name='melon',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique melon record'),
        ),
        migrations.AddConstraint(
            model_name='crowdtangleinstagram',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique instagram record'),
        ),
        migrations.AddConstraint(
            model_name='crowdtanglefacebook',
            constraint=models.UniqueConstraint(fields=('artist', 'recorded_date'), name='unique facebook record'),
        ),
    ]
