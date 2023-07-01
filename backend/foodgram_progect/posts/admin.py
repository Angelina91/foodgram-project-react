from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
    )
    list_filter = (
        'author',
        'name',
    )
    inlines = (
        IngredientInline,
    )


admin.site.register(Tag)

