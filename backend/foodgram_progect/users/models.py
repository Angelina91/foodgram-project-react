from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username_not_me


class User(AbstractUser):
    """Кастомный User с распределенными правами по ролям"""
    # USERNAME_FIELD = 'username'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    # USER_ROLE = 'user'
    # MODERATOR_ROLE = 'moderator'
    # ADMIN_ROLE = 'admin'

    # ROLE_CHOICES = (
    #     (USER_ROLE, 'user'),
    #     (MODERATOR_ROLE, 'moderator'),
    #     (ADMIN_ROLE, 'admin'),
    # )

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
        verbose_name='Логин пользователя',
        help_text='Ваш логин',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Ваш пароль',
    )

    # role = models.CharField(
    #     choices=ROLE_CHOICES,
    #     max_length=50,
    #     default='user',
    #     verbose_name='Роль пользователя',
    #     help_text='Выберите из списка роль для пользователя'
    # )

    # bio = models.TextField(
    #     max_length=250,
    #     blank=True,
    #     verbose_name='Роль пользователя',
    #     help_text='Выберите из списка роль для пользователя'
    # )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия пользователя',
        help_text='Введите Вашу фамилию',
    )

    is_subcribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на автора',
        help_text='Отметка о подписке на автора',
    )

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

    # @property
    # def is_admin(self):
    #     return self.role == User.ADMIN_ROLE or self.is_superuser

    # @property
    # def is_moderator(self):
    #     return self.role == User.MODERATOR_ROLE or self.is_staff
