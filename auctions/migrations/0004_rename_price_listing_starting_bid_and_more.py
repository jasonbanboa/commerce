# Generated by Django 4.1 on 2022-09-07 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='starting_bid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
    ]
