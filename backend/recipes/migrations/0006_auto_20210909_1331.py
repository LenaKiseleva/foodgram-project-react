# Generated by Django 3.0 on 2021-09-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210909_1331'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cart',
            name='unique_Cart',
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_Cart'),
        ),
    ]
