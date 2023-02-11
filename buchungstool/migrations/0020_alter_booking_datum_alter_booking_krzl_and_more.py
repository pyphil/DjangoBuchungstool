# Generated by Django 4.1.5 on 2023-02-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0001_squashed_0019_booking_series_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='datum',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='krzl',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='booking',
            name='stunde',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='card',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='short_name',
            field=models.CharField(max_length=10),
        ),
    ]
