# Generated by Django 3.2.2 on 2021-05-09 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_brands', related_query_name='create_brand', to='user.user'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_brands', related_query_name='update_brand', to='user.user'),
        ),
    ]
