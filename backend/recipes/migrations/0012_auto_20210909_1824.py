# Generated by Django 3.0 on 2021-09-09 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20210909_1821'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]
