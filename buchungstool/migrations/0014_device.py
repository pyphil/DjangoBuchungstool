# Generated by Django 4.0.2 on 2022-06-04 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0013_booking_pen_01_booking_pen_02_booking_pen_03_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=10)),
            ],
        ),
    ]
