# Generated by Django 4.2.1 on 2023-07-06 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesinvoice',
            old_name='room',
            new_name='booked_room',
        ),
    ]
