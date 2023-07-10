from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from posts.models import (FavoriteAuthor, FavoriteRecipe, Ingredient,
                          IngredientDetale, Recipe, ShoppingCart, Tag)
from rest_framework import exceptions, filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          PostRecipeSerializer, RecipeSerializer,
                          SubscriptionsSerializer, TagSerializer)


class CustomUserViewSet(UserViewSet):
    """ Пользователь с настройками подписки """

    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(
        detail=False,
        methods=['GET'],
        serializer_class=SubscriptionsSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = user.follower.all()
        authors = [item.author.id for item in user_subscriptions]
        queryset = User.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        serializer_class=SubscriptionsSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Нельзя подписаться на самого себя'
                )
            if FavoriteAuthor.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError(
                    'На этого автора уже есть подписка'
                )
            FavoriteAuthor.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)

            return Response(serializer.data, status=HTTPStatus.CREATED)

        if self.request.method == 'DELETE':
            if not FavoriteAuthor.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError(
                    'Нет такой подписки'
                )
            subscription = get_object_or_404(
                FavoriteAuthor,
                user=user,
                author=author
            )
            subscription.delete()

            return Response(status=HTTPStatus.NO_CONTENT)

        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Теги к рецепту """

    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(ReadOnlyModelViewSet):
    """ Ингредиенты для рецепта """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = IngredientFilter
    pagination_class = CustomPagination


class CreateListRetrieveDestroyViewSet(mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    """ Сериалайзер для ограничения методов """

    http_method_names = ['get', 'post', 'patch', 'delete']


class RecipeViewSet(CreateListRetrieveDestroyViewSet):
    """ Рецепт, выгрузка файла со списком """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return PostRecipeSerializer

    def post_delete(self, request, pk, database):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if not database.objects.filter(
                user=self.request.user,
                recipe=recipe,
            ).exists():
                database.objects.create(
                    user=self.request.user,
                    recipe=recipe)
                serializer = FavoriteRecipeSerializer(recipe)
                return Response(
                    serializer.data,
                    status=HTTPStatus.CREATED,
                )
            error_text = 'Рецепт уже добавлен'
            return Response(error_text, status=HTTPStatus.BAD_REQUEST)
        elif request.method == 'DELETE':
            if database.objects.filter(
                user=self.request.user,
                recipe=recipe,
            ).exists():
                database.objects.filter(
                    user=self.request.user,
                    recipe=recipe,
                ).delete()
                return Response(status=HTTPStatus.NO_CONTENT)
            error_text = 'Такого объекта нет в списке'
            return Response(error_text, status=HTTPStatus.NO_CONTENT)
        else:
            error_text = 'Выбран неверный метод запроса'
            return Response(error_text, status=HTTPStatus.BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.post_delete(request, pk, FavoriteRecipe)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.post_delete(request, pk, ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        shop_list = IngredientDetale.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )
        shop_list_text = 'Список покупок'
        for item in shop_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            shop_list_text += (
                f'Наименование: {ingredient.name}, количество {amount} '
                f'{ingredient.measurement_unit}\n'
            )

        response = HttpResponse(shop_list_text, content_type='application/pdf')
        response['Content-disposition'] = (
            'attachment; filename=shopping-list.pdf'
        )
        return response
