# Generated by Django 4.2.2 on 2023-07-08 00:14

import AppFutbolArg.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFutbolArg', '0011_alter_avatar_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=AppFutbolArg.models.avatar_image_path),
        ),
    ]
