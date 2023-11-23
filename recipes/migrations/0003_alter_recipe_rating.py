# Generated by Django 3.2.23 on 2023-11-21 21:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20231119_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, message='Rating must be at least 1.'), django.core.validators.MaxValueValidator(5, message='Rating must be at most 5.')]),
        ),
    ]