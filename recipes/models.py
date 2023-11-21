from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    instructions = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name="liked_recipes", blank=True)
    prep_time = models.IntegerField(blank=True, null=True)
    cook_time = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(default=1)
    rating = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating must be at most 5."),
        ])
    total_ratings = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-title']
    
    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_reviews(self):
        return self.reviews.count()

    def rate_recipe(self, user, rating):
        # ensuring the rating is between 1 and 5
        rating = max(1, min(5, rating))
        # Update the rating and total_ratings
        self.rating = round((self.rating * self.total_ratings + rating) / (self.total_ratings + 1), 2)
        self.total_ratings += 1
        # save the changes
        self.save()

    def average_rating(self):
        return self.rating

    def get_adjusted_ingredients(self, desired_servings):
        adjusted_ingredients = []
        for ingredient in self.ingredients.all():
            adjusted_quantity = (ingredient.quantity / self.servings) * desired_servings
            adjusted_ingredients.append({
                'name': ingredient.name,
                'quantity': adjusted_quantity,
                'unit': ingredient.unit,
            })
        return adjusted_ingredients


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Review {self.body} by {self.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    quantity=models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"


