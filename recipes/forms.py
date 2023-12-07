from .models import Review, Recipe, RecipeIngredient
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('rating',)


class AddIngredientForm(forms.ModelForm):

    UNIT_CHOICES = [
        ("gram", "gram"),
        ("kilogram", "kg"),
        ("mililiter", "ml"),
        ("liter", "ltr"),
    ]
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']

    unit = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=UNIT_CHOICES,
    )


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use inlineformset_factory to create the formset
        IngredientFormSet = inlineformset_factory(
            Recipe,
            RecipeIngredient,
            form=AddIngredientForm,
            extra=25,
            min_num=1,
            validate_min=True,
            can_delete=True,
            can_delete_extra = True,
        )

        # Pass instance=self.instance to formset to link it to the Recipe instance
        self.ingredient_formset = IngredientFormSet(*args, **kwargs, instance=self.instance)

         # Add class to the formset fields
        for form in self.ingredient_formset.forms:
            form.fields['name'].widget.attrs['class'] = 'ingredient-name'
            form.fields['quantity'].widget.attrs['class'] = 'ingredient-quantity'
            form.fields['unit'].widget.attrs['class'] = 'ingredient-unit'
            form.fields['DELETE'].required = False
        

    # instruction_step = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'steps'})
    # )

    # instructions = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'instruction-steps', 'type': 'hidden'})
    # )

    # def clean_instructions(self):
    #     instruction_step = self.cleaned_data['instruction_step']
    #     instruction_text = self.cleaned_data['instruction_text']

    #     instructions = f'{instruction_step} {instruction_text}'
    #     return instructions
    # ---------------------------------------------->

    # prep_time = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'positive-number'}),
    #     min_value=0
    # )
    # cook_time = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'positive-number'}),
    #     min_value=0
    # )

    # servings = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'positive-number'}),
    #     min_value=0
    # )

    # def clean_prep_time(self):
    #     prep_time = self.cleaned_data['prep_time']
    #     if prep_time < 0:
    #         raise forms.ValidationError("Prep time must be a positive number.")
    #     return prep_time

    # def clean_cook_time(self):
    #     cook_time = self.cleaned_data['cook_time']
    #     if cook_time < 0:
    #         raise forms.ValidationError("Cook time must be a positive number.")
    #     return cook_time

    # def clean_servings(self):
    #     servings = self.cleaned_data['servings']
    #     if servings < 0:
    #         raise forms.ValidationError("Servings must be a positive number.")
    #     return servings
    
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if Recipe.objects.filter(title=title).exists():
    #         raise forms.ValidationError("The recipe name already exists. Please provide a different name!")
    #     return title

    # def clean(self):
    #     cleaned_data = super().clean()

    #     title = cleaned_data.get('title')
    #     instructions = cleaned_data.get('instructions')
    #     # Add more fields as needed

    #     # Your custom validation or cleaning logic here

    #     return cleaned_data


class UpdateRecipeForm(forms.ModelForm):
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



