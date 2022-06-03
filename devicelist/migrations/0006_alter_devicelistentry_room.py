# Generated by Django 4.0.2 on 2022-06-03 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0013_booking_pen_01_booking_pen_02_booking_pen_03_and_more'),
        ('devicelist', '0005_rename_device_devicelistentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicelistentry',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='buchungstool.room'),
        ),
    ]
