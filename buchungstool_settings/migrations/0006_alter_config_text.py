# Generated by Django 4.1.5 on 2023-01-11 20:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buchungstool_settings', '0005_alter_config_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
