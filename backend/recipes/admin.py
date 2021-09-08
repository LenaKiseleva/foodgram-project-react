from django.contrib import admin
from import_export.admin import ImportMixin

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe)
from recipes.resources import IngredientResource


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text', 'cooking_time', 'image')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'recipe')


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    # For import csv files
    resource_class = IngredientResource


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
