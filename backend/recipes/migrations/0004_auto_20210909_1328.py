# Generated by Django 3.0 on 2021-09-09 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210908_1733'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_IngredientRecipe'),
        ),
    ]
