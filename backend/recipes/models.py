from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    author =  models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        unique=True,
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=1,
        validators=[
            MinValueValidator(1, message='Минимальное время 1 мин.')
        ],
    )
    image = models.ImageField(
        upload_to='upload/',
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
    )
    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name} от {self.author}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения ингредиента',
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название тега',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        unique=True,
    )
    slug = models.SlugField(
        max_length=10,
        unique=True,
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients_in',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(1, message='Минимальное количество 1')
        ],
    )

    def get_amount(self):
        return self.amount


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_in',    
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_in',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_TagRecipe'
            )
        ]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscriber'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase_recipe'
    )