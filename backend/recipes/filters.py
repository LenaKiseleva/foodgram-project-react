import django_filters

from recipes.models import Recipe


# class RecipesFilter(django_filters.FilterSet):
#     tags = django_filters.CharFilter(
#         field_name='tags__slug',
#     )

#     # is_favorited = django_filters.BooleanFilter(
#     #     field_name='favorite_recipe__recipe',
#     #     method='filter_is_favorited',
#     #     lookup_expr='isnull'
#     # )

#     # def filter_is_favorited(self, queryset, name, value):
#     #     lookup = '__'.join([name, 'isnull'])
#     #     user = self.request.user
#     #     favor = (user.favorite_subscriber.all())
#     #     print(queryset)
#     #     print(favor)
#     #     return queryset.filter(favorite_recipe=favor[0], **{lookup: not(value)})


#     class Meta:
#         model = Recipe
#         fields = ['tags']


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