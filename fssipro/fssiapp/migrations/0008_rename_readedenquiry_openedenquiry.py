# Generated by Django 5.0.1 on 2024-02-01 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fssiapp', '0007_readedenquiry'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReadedEnquiry',
            new_name='OpenedEnquiry',
        ),
    ]