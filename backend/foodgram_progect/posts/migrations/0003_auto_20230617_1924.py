# Generated by Django 3.2 on 2023-06-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230617_1923'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='shoppingcart',
            name='unique_shopping_list',
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
    ]
