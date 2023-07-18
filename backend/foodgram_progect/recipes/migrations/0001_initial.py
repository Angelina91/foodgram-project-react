# Generated by Django 3.2 on 2023-07-15 13:04

import colorfield.fields
import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ингредиента', max_length=100, unique=True, verbose_name='Ингредиент')),
                ('measurement_unit', models.CharField(help_text='Единица измерения', max_length=50, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientDetale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Количество ингредиентов', max_digits=3, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Маловато будет')], verbose_name='Количество ингредиентов')),
                ('ingredient', models.ForeignKey(help_text='Ингредиент', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_detale', to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент для рецепта',
                'verbose_name_plural': 'Ингредиенты для рецептов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Картинка, закодированная в Base64', upload_to='', verbose_name='Картинка, закодированная в Base64')),
                ('text', models.TextField(help_text='Описание', verbose_name='Описание')),
                ('cooking_time', models.PositiveIntegerField(default=1, help_text='Время приготовления (в минутах)', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации', verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Автор рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('ingredients', models.ManyToManyField(help_text='Список ингредиентов', related_name='recipes', through='recipes.IngredientDetale', to='recipes.Ingredient', verbose_name='Список ингредиентов')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название Тега', max_length=200, unique=True, verbose_name='Тег')),
                ('color', colorfield.fields.ColorField(default='#F869D5', help_text='Hex-code', image_field=None, max_length=7, samples=None, unique=True, verbose_name='Hex-code')),
                ('slug', models.SlugField(error_messages={'name': {'max_length': 'Слишком длинный слаг'}}, help_text='slug', max_length=200, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт в списке покупок', on_delete=django.db.models.deletion.CASCADE, related_name='in_shopping_cart', to='recipes.recipe', verbose_name='Рецепт в списке покупок')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='in_shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупки',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Список id тегов', related_name='recipes', to='recipes.Tag', verbose_name='Список id тегов'),
        ),
        migrations.AddField(
            model_name='ingredientdetale',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_detale', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Избранный рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='in_favorite', to='recipes.recipe', verbose_name='Избранный рецепт')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_list', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
            },
        ),
        migrations.CreateModel(
            name='FavoriteAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(help_text='Избранный автор', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Избранный автор')),
                ('user', models.ForeignKey(help_text='Подписчик', on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка на избранного автора',
                'verbose_name_plural': 'Подписки на избранных авторов',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientdetale',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='ingredient_for_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='favorite_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favoriteauthor',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='no_self_subscribe'),
        ),
        migrations.AddConstraint(
            model_name='favoriteauthor',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_subscription'),
        ),
    ]
