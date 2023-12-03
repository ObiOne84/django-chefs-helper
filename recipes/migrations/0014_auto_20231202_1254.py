# Generated by Django 3.2.23 on 2023-12-02 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_recipe_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredient',
            name='recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.RecipeIngredient'),
        ),
    ]
