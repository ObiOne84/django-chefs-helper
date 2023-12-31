from django.test import TestCase
from django.contrib.auth.models import User
from . import views
from django.db import IntegrityError
from decimal import Decimal
from django.urls import reverse
from .models import Recipe


# source: CI - Django test module
class RecipeListViewTest(TestCase):
    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe_images'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes.html')


class RecipeDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user
        )

    def test_recipe_details_view_reviews(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse(
            'recipe_detail', args=[self.recipe.slug]),
            {'body': 'Great recipe!'}
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe_images'))
        self.assertTrue(
            self.recipe.reviews.filter(body='Great recipe!').exists()
            )

    def test_like_recipe(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse(
            'recipe_like',
            args=[self.recipe.slug]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.recipe.likes.filter(id=self.user.id).exists())

    def test_rate_recipe(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse(
            'recipe_detail',
            args=[self.recipe.slug]),
            {'rating': 4}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.recipe.rated_users.filter(
            id=self.user.id).exists()
        )

    def test_unregistered_user_redirect_to_login(self):
        response = self.client.get(reverse(
            'recipe_detail', args=[self.recipe.slug])
            )
        self.assertEqual(response.status_code, 302)
