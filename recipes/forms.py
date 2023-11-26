from .models import Review, Recipe
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('rating',)
