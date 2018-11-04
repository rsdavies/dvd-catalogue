# Generated by Django 2.1 on 2018-11-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dvd',
            name='poster_url',
            field=models.URLField(default='none'),
        ),
        migrations.AddField(
            model_name='dvd',
            name='rotten_tomato_rating',
            field=models.PositiveSmallIntegerField(default=999),
        ),
        migrations.AddField(
            model_name='dvd',
            name='runtime',
            field=models.PositiveSmallIntegerField(default=999),
        ),
    ]