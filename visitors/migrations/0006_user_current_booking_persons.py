# Generated by Django 4.2.2 on 2023-06-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0005_rename_date_from_booking_check_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_booking_persons',
            field=models.IntegerField(default=2),
        ),
    ]
