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

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'instructions',
            'featured_image',
            'excerpt',
            'prep_time',
            'cook_time',
            'servings',
            'status',
            ]
        # instructions = forms.CharField(widget=forms.Textarea(attrs={'class': 'instructions-input'}))
    prep_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0
    )
    cook_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0
    )
    servings = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0
    )

    def clean_prep_time(self):
        prep_time = self.cleaned_data['prep_time']
        if prep_time < 0:
            raise forms.ValidationError("Prep time must be a positive number.")
        return prep_time

    def clean_cook_time(self):
        cook_time = self.cleaned_data['cook_time']
        if cook_time < 0:
            raise forms.ValidationError("Cook time must be a positive number.")
        return cook_time

    def clean_servings(self):
        servings = self.cleaned_data['servings']
        if servings < 0:
            raise forms.ValidationError("Servings must be a positive number.")
        return servings
