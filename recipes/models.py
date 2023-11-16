from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


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
    likes = models.ManyToManyField(User, related_name="liked_recipes")
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField(default=1)
    rating = models.IntegerField(default=0)
    total_ratings = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-title']
    
    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def average_rating(self):
        return self.rating
