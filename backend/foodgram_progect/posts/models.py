from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
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
    tag = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тег',
        help_text='Тег',
    )
    food_pre_time = models.PositiveIntegerField( # уточнить про это поле, если будут ошибки
        # слишком просто че-т
        verbose_name='Время приготовления',
        help_text='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата публикации"
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

class Tag(models.Model):
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

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории's

# Create your models here.
