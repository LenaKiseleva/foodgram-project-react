import django_filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags',
                  'author',
                  'is_favorited',
                  'is_in_shopping_cart'
                  )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                purchase_recipe__user=self.request.user
            )
        return Recipe.objects.all().exclude(
            purchase_recipe__user=self.request.user
        )

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(
                favorite_recipe__user=self.request.user
            )
        return Recipe.objects.all().exclude(
            favorite_recipe__user=self.request.user
        )


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit',)
