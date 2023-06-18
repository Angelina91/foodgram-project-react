# Generated by Django 3.2 on 2023-06-08 18:15

from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, help_text='Ваш логин', max_length=150, unique=True, validators=[users.validators.validate_username_not_me], verbose_name='Логин пользователя'),
        ),
    ]
