# Generated by Django 3.2.2 on 2021-11-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0009_place_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='telephone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
