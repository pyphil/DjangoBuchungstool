# Generated by Django 4.0.2 on 2022-04-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlist', '0002_remove_userlist_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlist',
            name='krzl',
            field=models.CharField(default='Null', max_length=3),
            preserve_default=False,
        ),
    ]
