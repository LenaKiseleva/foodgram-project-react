from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (IngredientViewSet, RecipeViewSet, favorite,
                           shopping_cart, TagViewSet)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='Recipe')
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('tags', TagViewSet, basename='Tag')


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/shopping_cart/', shopping_cart),
    path('recipes/<int:pk>/favorite/', favorite),
]
