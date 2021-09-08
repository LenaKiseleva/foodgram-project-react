from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from users.models import Subscribe, User
from users.serializers import UserSerializer

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class GetRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    image = Base64ImageField(read_only=True, use_url=True)
    cooking_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class GetFavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)


class GetCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ('user', 'recipe',)


class TagRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source='tag.id')
    name = serializers.CharField(required=False, source='tag.name')
    color = serializers.CharField(required=False, source='tag.color')
    slug = serializers.SlugField(required=False, source='tag.slug')
    class Meta:
        model = TagRecipe
        fields = ('id', 'name', 'color', 'slug',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient.id')
    name = serializers.CharField(required=False, source='ingredient.name')
    measurement_unit = serializers.CharField(required=False, source='ingredient.measurement_unit')
    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, obj):
        return obj.id


class AuthorSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Subscribe.objects.filter(author=obj.id, user=user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagRecipeSerializer(source='tags_in', many=True)
    author = AuthorSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(source='ingredient_in', many=True)
    is_favorited = serializers.SerializerMethodField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(default=False)
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.IntegerField(required=True)
    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(recipe_id=obj.id, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Cart.objects.filter(recipe_id=obj.id, user=user).exists()


class CreateIngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient.id')
    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)

    def get_id(self, obj):
        return obj.id


class CreateOrUpdateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = CreateIngredientsRecipeSerializer(many=True, source='ingredient_in')
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = UserSerializer(read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image', 'name',  'text', 'cooking_time',)

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context=self.context)
        return serializer.data

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredient_in")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
               id=ingredient['ingredient']['id'].id)

            IngredientRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=ingredient['amount'])
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredient_in')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                instance.cooking_time)
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.tags.set(tags_data)
        recipe = Recipe.objects.filter(id=instance.id)
        recipe.update(**validated_data)
        for new_ingredient_data in ingredients_data:
            amount = new_ingredient_data['amount']
            if amount < 1:
                raise serializers.ValidationError(
                    'Убедитесь, что это значение больше 0.'
                )
            ingredient_instance = get_object_or_404(
                Ingredient, pk=new_ingredient_data['ingredient']['id'].id
            )
            IngredientRecipe.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient_instance,
                amount=amount
            )
        return instance
