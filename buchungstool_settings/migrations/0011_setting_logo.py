# Generated by Django 4.1.5 on 2023-02-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool_settings', '0010_rename_school_setting_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='logo',
            field=models.FileField(blank=True, upload_to='logo/'),
        ),
    ]
