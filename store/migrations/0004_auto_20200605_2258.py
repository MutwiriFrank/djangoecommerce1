# Generated by Django 2.2.8 on 2020-06-05 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200604_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='location',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='landmark',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='road',
            new_name='state',
        ),
    ]
