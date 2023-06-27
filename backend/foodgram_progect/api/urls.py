from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet, SubscriptionsView)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'v1/users/<int:id>/subscriptions/',
        SubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
