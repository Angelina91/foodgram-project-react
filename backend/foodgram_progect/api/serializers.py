from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (FavoriteAuthor, FavoriteRecipe, Ingredient,
                            IngredientDetale, Recipe, ShoppingCart, Tag)
from rest_framework import exceptions, serializers
from rest_framework.fields import (IntegerField, ReadOnlyField,
                                   SerializerMethodField)
from users.models import User


class CreateUserSerializer(UserCreateSerializer):
    """ Создание пользователя """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'wrtite_only': True}}


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для модели пользователя """

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoriteAuthor.objects.filter(
            user=user,
            author=obj
        ).exists()

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


class SubscriptionsSerializer(CustomUserSerializer):
    """ Подписка на автора """

    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count',
        read_only=True,
    )

    def get_recipes(self, obj):
        author_recipes = Recipe.objects.filter(author=obj)
        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author_recipes = author_recipes[:int(recipes_limit)]
        return []

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор Тэгов """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Ингредиенты """

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientDetaleSerializer(serializers.ModelSerializer):
    """ Ингредиенты для рецепта """

    id = IntegerField(write_only=True)
    amount = IntegerField(write_only=True)

    class Meta:
        model = IngredientDetale
        fields = ('id', 'amount')


class GetIngredientSerializer(serializers.ModelSerializer):
    """ Получение ингредиентов из рецепта """

    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientDetale
        fields = ('id', 'name', 'amount', 'measurement_unit',)


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериалайзер модели Рецепт """

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer()
    image = Base64ImageField()
    ingredients = GetIngredientSerializer(many=True,
                                          read_only=True,
                                          source='amount_ingredient')
    is_favorite = SerializerMethodField(
        method_name='get_is_favorite',
        read_only=True,
    )
    is_in_shopping_cart = SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'text',
            'tags',
            'cooking_time',
            'author',
            'pub_date',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
        )

    def get_is_favorite(self, obj):
        user = self.context['request'].user.id
        recipe = obj.id
        return FavoriteRecipe.objects.filter(
            user_id=user,
            recipe_id=recipe,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user.id
        recipe = obj.id
        return ShoppingCart.objects.filter(
            user_id=user,
            recipe_id=recipe,
        ).exists()


class PostRecipeSerializer(serializers.ModelSerializer):
    """ Публикация рецепта """

    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = IngredientDetaleSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        if not tags or not ingredients:
            raise ValidationError(
                'Минимум: 1 ингредиент и 1 тег'
            )
        ingredient_id = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_id) != len(set(ingredient_id)):
            raise ValidationError(
                'Ингредиенты не должны повторться в рецепте'
            )
        data.update(
            {
                'tags': tags,
                'ingredients': ingredients,
            }
        )
        return data

    def add_tags_ingredients(self, tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        for ingredient in ingredients:
            IngredientDetale.objects.create(
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
        return recipe

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_tags_ingredients(
            tags,
            ingredients,
            recipe,
        )

    @transaction.atomic
    # def update(self, instanse, validated_data):
    #     instanse.tags.clear()
    #     instanse.ingredients.clear()
    #     tags = validated_data.pop('tags')
    #     ingredients = validated_data.pop('ingredients')
    #     instanse = super().update(instanse, validated_data)
    #     return self.add_tags_ingredients(
    #         tags,
    #         ingredients,
    #         instanse,
    #     )

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """ Избранный рецепт """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'cooking_time',
        )
