# Generated by Django 4.1 on 2022-09-08 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_listing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.CharField(default='test', max_length=64),
        ),
    ]
