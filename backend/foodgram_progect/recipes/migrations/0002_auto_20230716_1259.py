# Generated by Django 3.2 on 2023-07-16 12:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientdetale',
            name='amount',
            field=models.PositiveIntegerField(default=1, help_text='Количество ингредиентов', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Маловато будет')], verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='slug', max_length=200, unique=True, verbose_name='slug'),
        ),
    ]
