# Generated by Django 3.1.4 on 2022-01-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadinfo', '0004_auto_20220117_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='latest_koatuu',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
