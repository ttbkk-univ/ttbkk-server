# Generated by Django 3.2.2 on 2021-05-13 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0004_alter_place_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
