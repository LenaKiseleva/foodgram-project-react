from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.filters import RecipeFilter
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from recipes.serializers import (CreateOrUpdateRecipeSerializer,
                                 GetCartSerializer, GetFavoriteSerializer,
                                 GetRecipeSerializer, IngredientSerializer,
                                 RecipeSerializer, TagSerializer)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite(request, pk):
    if request.method == "GET":
        favor, created = Favorite.objects.get_or_create(user=request.user, recipe_id=pk)
        if created:
            serializer = GetFavoriteSerializer(favor, context={'request': request})
            recipe = Recipe.objects.get(id=pk)
            serializer_for_create = GetRecipeSerializer(recipe, context={'request': request})
            return Response(serializer_for_create.data, status=status.HTTP_201_CREATED)
        return Response({'errors': 'Рецепт уже в избранном'}, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        favor = get_object_or_404(Favorite, user=request.user, recipe_id=pk)
        favor.delete()
        return Response({'detail': 'Рецепт удален из избранного'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def shopping_cart(request, pk):
    if request.method == "GET":
        cart, created = Cart.objects.get_or_create(user=request.user, recipe_id=pk)
        if created:
            serializer = GetCartSerializer(cart, context={'request': request})
            recipe = Recipe.objects.get(id=pk)
            serializer_for_create = GetRecipeSerializer(recipe, context={'request': request})
            return Response(serializer_for_create.data, status=status.HTTP_201_CREATED)
        return Response({'errors': 'Рецепт уже в корзине'}, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        cart = get_object_or_404(Cart, user=request.user, recipe_id=pk)
        cart.delete()
        return Response({'detail': 'Рецепт удален из корзины'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['tags']
    filter_class = RecipeFilter

    # def get_queryset(self, request, *args, **kwargs):
    #     queryset = super().get_queryset(self, request, *args, **kwargs)

    #     queryset = queryset # TODO
    #     return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateOrUpdateRecipeSerializer

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author=self.request.user)


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    pagination_class = None


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    pagination_class = None
