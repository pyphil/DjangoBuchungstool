# Generated by Django 4.1.5 on 2023-02-12 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool_settings', '0007_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
