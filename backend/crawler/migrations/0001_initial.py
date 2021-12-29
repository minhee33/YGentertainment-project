# Generated by Django 3.2.10 on 2021-12-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrowdtangleFacebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100, null=True)),
                ('followers', models.BigIntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrowdtangleInstagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.BigIntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Melon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('listeners', models.BigIntegerField()),
                ('streams', models.BigIntegerField()),
                ('fans', models.IntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url1', models.TextField(null=True)),
                ('url2', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTiktok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField()),
                ('uploads', models.IntegerField()),
                ('likes', models.BigIntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTwitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField()),
                ('twits', models.IntegerField()),
                ('user_created', models.TextField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeTwitter2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('followers', models.IntegerField()),
                ('twits', models.IntegerField()),
                ('user_created', models.TextField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialbladeYoutube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('uploads', models.IntegerField()),
                ('subscribers', models.IntegerField()),
                ('views', models.BigIntegerField()),
                ('user_created', models.TextField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('monthly_listens', models.BigIntegerField()),
                ('followers', models.BigIntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url1', models.TextField(null=True)),
                ('url2', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vlive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('members', models.IntegerField()),
                ('videos', models.IntegerField()),
                ('likes', models.BigIntegerField()),
                ('plays', models.BigIntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weverse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('weverses', models.IntegerField()),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
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
