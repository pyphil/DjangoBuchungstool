# Generated by Django 4.0.2 on 2022-03-05 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool', '0005_rename_buchung_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('room', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=20)),
            ],
        ),
    ]
