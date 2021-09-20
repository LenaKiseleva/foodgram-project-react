from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from recipes.paginations import CustomPagination
from recipes.serializers import (CreateOrUpdateRecipeSerializer,
                                 GetRecipeSerializer, IngredientSerializer,
                                 RecipeSerializer, TagSerializer)


class FavoriteDetail(APIView):
    """
    Добавление и удаление из избранного
    """
    def get(self, request, pk):
        favor, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=pk
        )
        if created:
            recipe = get_object_or_404(Recipe, id=pk)
            serializer_for_create = GetRecipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                serializer_for_create.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'errors': 'Рецепт уже в избранном'},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, pk, format=None):
        favor = get_object_or_404(Favorite, user=request.user, recipe_id=pk)
        favor.delete()
        return Response(
            {'detail': 'Рецепт удален из избранного'},
            status=status.HTTP_204_NO_CONTENT,
        )


class ShoppingCartDetail(APIView):
    """
    Добавление и удаление из корзины покупок
    """
    def get(self, request, pk):
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            recipe_id=pk
        )
        if created:
            recipe = get_object_or_404(Recipe, id=pk)
            serializer = GetRecipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'errors': 'Рецепт уже в корзине'},
            status=status.HTTP_201_CREATED,
            )

    def delete(self, request, pk, format=None):
        cart = get_object_or_404(Cart, user=request.user, recipe_id=pk)
        cart.delete()
        return Response(
            {'detail': 'Рецепт удален из корзины'},
            status=status.HTTP_204_NO_CONTENT
        )


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                cart = self.request.query_params.get(
                    'is_in_shopping_cart',
                    None,
                )
                if cart is not None:
                    self._paginator = CustomPagination()
                else:
                    self._paginator = self.pagination_class()
        return self._paginator

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if ('is_in_shopping_cart' in self.request.query_params and
           self.request.query_params['is_in_shopping_cart'] == 'true'):
            queryset = queryset.filter(purchase_recipe__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateOrUpdateRecipeSerializer

    def perform_create(self, serializer, *args, **kwargs):
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)
        return serializer.errors

    def perform_update(self, serializer, *args, **kwargs):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return serializer.errors

    @action(
        methods=['get', ],
        detail=False,
        url_path='download_shopping_cart',
        url_name='download_shopping_cart')
    def download_shopping_cart(self, request):
        shoping_list = {}
        carts = get_list_or_404(Cart, user_id=request.user.id)
        for cart in carts:
            recipes = get_list_or_404(Recipe, id=cart.recipe_id)
            for recipe in recipes:
                ings = get_list_or_404(
                    IngredientRecipe,
                    recipe_id=recipe.id
                )
                for ing in ings:
                    if ing.ingredient_id not in shoping_list:
                        shoping_list[ing.ingredient_id] = ing.amount
                    else:
                        shoping_list[ing.ingredient_id] += ing.amount
        content = []
        for i in shoping_list:
            ingredient = get_object_or_404(Ingredient, id=i)
            content.append(f'{ingredient.name}: '
                           f'{shoping_list[i]} '
                           f'{ingredient.measurement_unit}.\n')
        response = HttpResponse(content, content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=shopping-list'
        return response


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    filter_class = IngredientFilter
    pagination_class = None


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    pagination_class = None
