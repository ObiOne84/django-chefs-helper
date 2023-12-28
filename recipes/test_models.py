from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Review, RecipeIngredient
from django.db import IntegrityError
from decimal import Decimal


# Make sure to switch to local database to perform automated tests (setting.py)
class RecipeModelTestCase(TestCase):
    def setUp(self):
        # Create Test User
        self.user = User.objects.create_user(
            username="John",
            password='john&2023!'
            )

        # Create Test Recipe
        self.recipe = Recipe.objects.create(
            title='Recipe Test',
            slug='recipe-test',
            author=self.user,
            instructions='Recipe instructions',
            featured_image='placeholder',
            excerpt='Recipe excerpt',
            prep_time=10,
            cook_time=20,
            servings=4,
            rating=5,
            total_ratings=1,
            sum_of_rating=5,
            status=0,
        )

    # Test recipe name
    def test_title(self):
        self.assertEqual(self.recipe.title, 'Recipe Test')

    # Test unique title and slug fields
    def test_unique_title_and_slug(self):
        with self.assertRaises(IntegrityError):
            copy_recipe = Recipe.objects.create(
                title='Recipe Test',
                slug='recipe-test',
                author=self.user,
                instructions='Copy recipe instructions',
                featured_image='placeholder',
                excerpt='Copy recipe excerpt',
                prep_time=5,
                cook_time=10,
                servings=4,
                rating=3,
                total_ratings=5,
                status=1,
            )

    # Test if the recipe deletes with the author
    def test_recipe_deleted_with_author(self):
        self.assertTrue(Recipe.objects.filter(title='Recipe Test').exists())
        self.user.delete()
        self.assertFalse(Recipe.objects.filter(title='Recipe Test').exists())

    # Test number of likes
    def test_number_of_likes(self):
        self.assertEqual(self.recipe.number_of_likes(), 0)
        self.recipe.likes.add(self.user)
        self.assertEqual(self.recipe.number_of_likes(), 1)

    # Test rate the recipe
    def test_rate_recipe(self):
        # Test that the rate_recipe method updates the recipe's ratings
        self.recipe.rate_recipe(self.user, 4)
        self.assertEqual(self.recipe.total_ratings, 2)
        self.assertEqual(self.recipe.sum_of_rating, 9)

    # Test the string method __str__
    def test_recipe_string_method_returns_name(self):
        self.assertEqual(str(self.recipe), 'Recipe Test')

    # Test number of reviews method
    def test_number_of_reviews(self):
        self.assertEqual(self.recipe.number_of_reviews(), 0)
        review1 = Review.objects.create(
                recipe=self.recipe,
                name='Adam',
                email='adam@email.com',
                body='First review',
                approved=True,
        )
        review2 = Review.objects.create(
                recipe=self.recipe,
                name='Tom',
                email='Tom@email.com',
                body='Second review',
                approved=True,
        )
        review3 = Review.objects.create(
                recipe=self.recipe,
                name='Anna',
                email='anna@email.com',
                body='Third review',
                approved=True,
        )
        self.assertEqual(self.recipe.number_of_reviews(), 3)

    # Test __str__ for reviews
    def test_review_string_method_returns_body_and_name(self):
        review = Review.objects.create(
            recipe=self.recipe,
            name='Adam',
            email='adam@email.com',
            body='First review',
            approved=True,
        )
        self.assertEqual(str(review), 'Review First review by Adam')

    # Test __str__ for RercipeIngredient
    def test_ingredient_string_method_returns_body_and_name(self):
        # Creat test ingredient variable
        ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            name='Black Pepper',
            quantity=100,
            unit='grams',
        )
        self.assertEqual(str(ingredient), '100 grams Black Pepper')

    # Test calculate_average_rating with some sample ratings
    def test_calculate_average_rating_with_ratings(self):
        self.recipe.rate_recipe(self.user, 3)
        self.assertEqual(self.recipe.calculate_average_rating(), 4)
