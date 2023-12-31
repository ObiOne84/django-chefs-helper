from .models import Review, Recipe, RecipeIngredient
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from cloudinary.models import CloudinaryResource


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
        ("gram", "gm"),
        ("kilogram", "Kg"),
        ("mililiter", "ml"),
        ("liter", "Ltr"),
        ("unit", "unit"),
        ("teaspoon", "tsp"),
        ("tablespoon", "Tbsp"),
    ]

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']

    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'add-recipe-fields ingredient-name',
            'placeholder': 'Ingredient name...',
        }),
    )

    unit = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'unit-field bm-2',
        }),
        choices=UNIT_CHOICES,
    )

    quantity = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'positive-number bm-1',
            'placeholder': 'Quantity...',
        }),
        min_value=0,
        max_digits=6,
        max_value=9999.99,
        decimal_places=2,
        required=True,
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

        self.fields['featured_image'].widget.attrs.update({
            'accept': 'image/*',
            'class': 'form-control form-field',
        })
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Add unique recipe title...',
            'maxlength': 50,
            'class': 'add-recipe-fields title-field form-field',
        })
        self.fields['excerpt'].widget.attrs.update({
            'placeholder': 'Provide short description...',
            'maxlength': 500,
            'class': 'add-recipe-fields description-field form-field',
        })
        self.fields['prep_time'].widget.attrs.update({
            'class': 'add-recipe-fields time-field form-field',
        })
        self.fields['cook_time'].widget.attrs.update({
            'class': 'add-recipe-fields time-field form-field',
        })
        self.fields['servings'].widget.attrs.update({
            'class': 'add-recipe-fields time-field form-field',
        })

        # Use inlineformset_factory to create the formset
        IngredientFormSet = inlineformset_factory(
            Recipe,
            RecipeIngredient,
            form=AddIngredientForm,
            extra=25,
            min_num=1,
            validate_min=True,
            can_delete=True,
            can_delete_extra=True,
        )

        # Source:https://docs.djangoproject.com/en/4.2/topics/forms/formsets/
        # Source:https://www.geeksforgeeks.org/django-formsets/
        # Source:https://justdjango.com/blog/dynamic-forms-in-django-htmx
        self.ingredient_formset = IngredientFormSet(
            *args,
            **kwargs,
            instance=self.instance,
            )

        for form in self.ingredient_formset.forms:
            form.fields['name'].widget.attrs.update({
                'class': 'ingredient-name form-field',
                'maxlength': 50,
            })
            form.fields['quantity'].widget.attrs['class'] = (
                'ingredient-quantity form-field'
            )
            form.fields['unit'].widget.attrs['class'] = 'ingredient-unit'
            form.fields['DELETE'].required = False

    prep_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0,
        max_value=600,
    )
    cook_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0,
        max_value=600,
    )

    servings = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=1,
        max_value=10,
    )

    def clean_prep_time(self):
        prep_time = self.cleaned_data['prep_time']
        if prep_time < 0:
            raise forms.ValidationError(
                "Prep time must be a positive number."
            )
        return prep_time

    def clean_cook_time(self):
        cook_time = self.cleaned_data['cook_time']
        if cook_time < 0:
            raise forms.ValidationError(
                "Cook time must be a positive number."
            )
        return cook_time

    def clean_servings(self):
        servings = self.cleaned_data['servings']
        if servings < 0:
            raise forms.ValidationError(
                "Servings must be a positive number."
            )
        return servings

    def clean_title(self):
        title = self.cleaned_data.get('title')
        title_lower = title.lower()

        if Recipe.objects.filter(title__iexact=title_lower).exists():
            raise forms.ValidationError(
                "The recipe name already exists."
                " Please provide a different name!"
            )
        return title

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        instructions = cleaned_data.get('instructions')

        return cleaned_data

    def clean_featured_image(self):
        featured_image = self.cleaned_data.get('featured_image', None)

        if featured_image is None or isinstance(featured_image, str):
            print("There is not image provided")
        else:
            max_size = 5 * 1024 * 1024
            if featured_image.size > max_size:
                raise ValidationError('Image size must be no more than 5 MB.')
        return featured_image


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['featured_image'].widget.attrs.update({
            'accept': 'image/*',
            'class': 'form-control',
        })
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Add unique recipe title...',
            'maxlength': 50,
            'class': 'add-recipe-fields title-field',
        })
        self.fields['excerpt'].widget.attrs.update({
            'placeholder': 'Provide short description...',
            'maxlength': 500,
            'class': 'add-recipe-fields description-field',
        })
        self.fields['prep_time'].widget.attrs.update({
            'class': 'add-recipe-fields time-field',
        })
        self.fields['cook_time'].widget.attrs.update({
            'class': 'add-recipe-fields time-field',
        })
        self.fields['servings'].widget.attrs.update({
            'class': 'add-recipe-fields time-field',
        })

    def clean_featured_image(self):
        featured_image = self.cleaned_data.get('featured_image', None)

        if featured_image and not isinstance(featured_image, str):
            if hasattr(
                    featured_image, 'file') and not featured_image.file.closed:
                max_size = 5 * 1024 * 1024

                if featured_image.size > max_size:
                    raise ValidationError(
                        'Image size must be no more than 5 MB.'
                    )

        return featured_image

    instructions = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'instruction-steps hide'
        }))

    prep_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0,
        max_value=600,
    )
    cook_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=0,
        max_value=600,
    )

    servings = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'positive-number'}),
        min_value=1,
        max_value=10,
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        instance = getattr(self, 'instance', None)

        if instance and title != instance.title:
            if Recipe.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    "The recipe name already exists."
                    " Please provide a different name!")
        return title
