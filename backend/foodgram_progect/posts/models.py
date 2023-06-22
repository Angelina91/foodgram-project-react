from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_measurement.models import MeasurementField
# from measurement.measures import Volume
from measurement.measures import Weight

User = get_user_model()


class Recipe(models.Model):
    """ Модель рецептов """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
        help_text='Автор рецепта',
    )

    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=150,
        help_text='Название рецепта',
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        help_text='Фото блюда',
    )
    text = models.TextField(
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    # slug = models.SlugField(max_length=50)
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientDetale',
        related_name='recipes',
        verbose_name='Ингредиенты для блюда',
        help_text='Ингредиенты для блюда',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тег',
        help_text='Тег',
    )
    cooking_time = models.PositiveIntegerField( 
        # слишком просто че-т
        verbose_name='Время приготовления',
        help_text='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата публикации",
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ Модель для тегов """

    name = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Тег',
        help_text='Название Тега',
    )
    color = ColorField(
        unique=True,
        format='hex',
        default='#F869D5',
        verbose_name='Hex-code',
        help_text='Hex-code',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug',
        help_text='slug',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """ Модель для ингридиентов """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Ингредиент',
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientDetale(models.Model):
    """ Промкжуточная модель для Ингредиентов и Рецептов"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_detale',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_detale',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    # amount = models.PositiveIntegerField(
    #     default='1',
    #     verbose_name='Количество ингредиентов',
    #     help_text='Количество ингредиентов',
    # )
    amount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов',
        help_text='Количество ингредиентов',
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='ingredient_for_recipe',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class FavoriteAuthor(models.Model):
    """ Промежуточная модель для подписки на автора """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
        help_text='Избранный автор',
    )

    class Meta:
        verbose_name = 'Подписка на избранного автора'
        verbose_name_plural = 'Подписки на избранных авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='favorite_author_for_user',
            )
        ]

    def __str__(self):
        return f'{self.author} for {self.user}'


class FavoriteRecipe(models.Model):
    """ Промежуточная модель для избранных рецептов """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Избранный рецепт',
        help_text='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_recipe',
            )
        ]

    def __str__(self):
        return f'{self.recipe} for {self.user}'


class ShoppingCart(models.Model): # shopping_cart
    """ Список покупок """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Рецепт в списке покупок',
        help_text='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Список покупки'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return f'{self.recipe} for {self.user}'
