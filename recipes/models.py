from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
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
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating must be at most 5."),
        ],
        default=0
        )
    total_ratings = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS, default=0)
    rated_users = models.ManyToManyField(User, related_name="rated_recipes", blank=True)

    class Meta:
        ordering = ['-title']
    
    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_reviews(self):
        return self.reviews.count()

    def rate_recipe(self, user, rating):
        if user not in self.rated_users.all():
            # ensuring the rating is between 1 and 5
            rating = max(1, min(5, rating))
            # Update the rating and total_ratings
            self.rating = round((self.rating * self.total_ratings + rating) / (self.total_ratings + 1), 1)
            self.total_ratings += 1
            # Add user to rated_users
            self.rated_users.add(user)
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

    
    # Source: https://studygyaan.com/django/how-to-create-a-unique-slug-in-django 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            count = 1
            while Recipe.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1

        super().save(*args, **kwargs)


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=500)
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


