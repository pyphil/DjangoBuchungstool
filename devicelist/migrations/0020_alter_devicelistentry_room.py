# Generated by Django 4.1.5 on 2023-04-10 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0028_room_is_first_of_category_room_is_last_of_category'),
        ('devicelist', '0019_alter_device_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicelistentry',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buchungstool.room'),
        ),
    ]
