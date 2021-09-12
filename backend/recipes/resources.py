from import_export import resources

from recipes.models import Ingredient


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        import_id_fields = ('name',)
        fields = ('name', 'measurement_unit')
