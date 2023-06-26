# from datetime import date
# from django.db.models import Avg
# from users.validators import validate_username_not_me
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from posts.models import (FavoriteAuthor, FavoriteRecipe, Ingredient,
                          IngredientDetale, Recipe, ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.fields import (IntegerField, ReadOnlyField,
                                   SerializerMethodField)
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from users.models import User


class CreateUserSerializer(UserCreateSerializer):
    """ Создание пользователя """

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'wrtite_only': True}}


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для модели пользователя """
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return FavoriteAuthor.objects.filter(
            user=user, author=obj
        ).exists() if user.is_authenticated else False

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

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    def get_recipes(self, obj):
        author = Recipe.objects.filter(author=obj)
        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author = author[:int(recipes_limit)]
        return []

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return FavoriteAuthor.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()


    class Meta:
        model = FavoriteAuthor
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteAuthor.objects.all(),
                fields=('user', 'author'),
            )
        ]


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
    # ingredients = serializers.SerializerMethodField()
    ingredients = GetIngredientSerializer(many=True,
                                          read_only=True,
                                          source='amount_ingredient')
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'text',
            'cooking_time',
            'author',
            'pub_date',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
        )

    # def get_ingredients(self, obj):
    #     recipe = obj
    #     ingredients = recipe.ingredients.values(
    #         'id',
    #         'name',
    #         'measurement_unit',
    #         amount=F('ingredient_detale__amount')

    #     )
    #     return ingredients

    def is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite_list.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.in_shopping_cart.filter(recipe=obj).exists()


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

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Без ингредиентов - никак!'
            )
        for ingredient in ingredients:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Нужен хотя бы один ингредиент'
                )
        ingredient_id = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_id) != len(set(ingredient_id)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторться в рецепте'
            )
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Нужен тэг для рецепта'
            )
        return tags

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

# class ContactForm(serializers.Serializer):
#     email = serializers.EmailField()
#     message = serializers.CharField()

#     def save(self):
#         email = self.validated_data['email']
#         message = self.validated_data['message']
#         send_email(from=email, message=message)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_tags_ingredients(
            tags,
            ingredients,
            recipe,
        )

    def update(self, instanse, validated_data):
        instanse.tags.clear()
        instanse.ingredients.clear()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instanse = super().update(instanse, validated_data)
        return self.add_tags_ingredients(
            tags,
            ingredients,
            instanse,
        )


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """ Избранный рецепт """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'cooking_time',
        )
# Example:def create(self, validated_data): email = validated_data.get("email", None) validated.pop("email") # Now you have a clean valid email string # You might want to call an external API or modify another table # (eg. keep track of number of accounts registered.) or even # make changes to the email format. # Once you are done, create the instance with the validated data return models.YourModel.objects.create(email=email, **validated_data)