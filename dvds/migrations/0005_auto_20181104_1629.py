# Generated by Django 2.1 on 2018-11-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvds', '0004_auto_20181104_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dvd',
            name='poster_url',
            field=models.URLField(default=0),
        ),
    ]
