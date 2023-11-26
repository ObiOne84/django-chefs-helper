from .models import Review, Recipe
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'body',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('rating',)
