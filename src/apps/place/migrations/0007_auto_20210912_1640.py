# Generated by Django 3.2.2 on 2021-09-12 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0006_auto_20210727_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(decimal_places=13, max_digits=15),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(decimal_places=12, max_digits=15),
        ),
    ]
