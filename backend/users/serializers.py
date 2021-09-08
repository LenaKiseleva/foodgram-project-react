from djoser.serializers import (CurrentPasswordSerializer, PasswordSerializer,
                                UserCreateSerializer, UserSerializer)
from recipes.models import Recipe
from recipes.serializers import GetRecipeSerializer
from rest_framework import serializers

from users.models import Subscribe, User


class UserSerializer(UserSerializer):
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


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = GetRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(default=False)
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count',
        )
    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author_id=obj.id).count()
        return recipes

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Subscribe.objects.filter(author=obj.id, user=user).exists()


class GetSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('user', 'author',)


class UserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
