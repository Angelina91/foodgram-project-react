# from datetime import date
# from django.db.models import Avg
# from users.validators import validate_username_not_me
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from posts.models import (FavoriteAuthor, FavoriteRecipe, Ingredient,
                          IngredientDetale, Recipe, ShoppingCart, Tag)
from users.models import User


class CreateUserSerializer(UserCreateSerializer):
    """ Создание пользователя """

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'wrtite_only': True}}


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для модели пользователя """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return FavoriteAuthor.objects.filter(
            user=user, author=obj
        ).exists() if user.is_authenticated else False

class SubscriptionsSerializer(serializers.ModelSerializer):
    """ Подписка на автора """

    class Meta:
        model = FavoriteAuthor
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteAuthor.objects.all(),
                fields=('user', 'author'),
            )
        ]
