# Generated by Django 4.0.2 on 2022-03-13 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0009_alter_booking_lerngruppe_alter_room_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='card',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
