from django.test import TestCase
from django.contrib.auth.models import User
from . import views
from django.db import IntegrityError
from decimal import Decimal
from django.urls import reverse
from .models import Recipe


class RecipeListViewTest(TestCase):
    # Test that the view returns a 200 status code.
    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe_images'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes.html')


class RecipeDetailsViewTest(TestCase):
    def setUp(self):
        # Create a recipe and a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(title='Test Recipe', author=self.user)

    def test_recipe_details_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe_detail', args=[self.recipe.slug]), {'body': 'Great recipe!'})
        
        # Check for a redirect (status code 302)
        self.assertEqual(response.status_code, 302)

        # You can also check the redirect target if needed
        self.assertRedirects(response, reverse('recipe_images'))

        # Add more specific tests for post request behavior
        self.assertTrue(self.recipe.reviews.filter(body='Great recipe!').exists())
        # Add similar tests for messages and other behavior
