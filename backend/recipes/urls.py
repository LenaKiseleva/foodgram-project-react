from django.urls import include, path

from rest_framework.routers import DefaultRouter

from recipes.views import (FavoriteDetail, IngredientViewSet, RecipeViewSet,
                           ShoppingCartDetail, TagViewSet)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='Recipe')
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('tags', TagViewSet, basename='Tag')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/favorite/', FavoriteDetail.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartDetail.as_view()),
]
