from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username_not_me


class User(AbstractUser):
    """ Кастомный User """

    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
    )
    username = models.CharField(
        max_length=150,
        db_index=True,
        unique=True,
        validators=[validate_username_not_me],
        verbose_name='Уникальный юзернейм',
        help_text='Ваш логин',
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Введите имя пользователя',
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя',
    )

    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Введите пароль',
    )

    # is_subcribed = models.BooleanField(
    #     default=False,
    #     verbose_name='Подписка на автора',
    #     help_text='Отметка о подписке на автора',
    # )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name',
            ),
        ]
        ordering = ('username',)
