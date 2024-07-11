# Generated by Django 5.0.6 on 2024-07-11 01:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serch', '0003_auto_20240709_1315'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='search_data',
            name='search_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='search_data',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='search_data',
            name='url',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='search_data',
            name='user',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
