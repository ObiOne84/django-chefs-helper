from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, Review, RecipeIngredient
from .forms import (
    ReviewForm, RecipeForm, AddRecipeForm, AddIngredientForm, UpdateRecipeForm
)
from django.db.models import Q
# from django.http import HttpResponseForbidden
import logging
from django.forms import inlineformset_factory


class RecipeList(generic.ListView):
    model = Recipe
    template_name = 'recipes.html'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        queryset_published = Recipe.objects.filter(
            status=1).order_by('-created_on')

        search_query = self.request.GET.get('recipe_name', '').lower()
        results_exist = True

        if user.is_authenticated:
            queryset_user_draft = Recipe.objects.filter(status=0, author=user)
            queryset = queryset_published | queryset_user_draft
            if search_query:
                queryset = queryset.filter(Q(title__icontains=search_query))

        else:
            queryset = queryset_published
            if search_query:
                queryset = queryset.filter(Q(title__icontains=search_query))

        if not queryset.exists():
            results_exist = False

        return queryset.order_by('-status', '-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('recipe_name', '')
        return context


class RecipeImages(RecipeList, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'recipes'


class RecipeDetails(LoginRequiredMixin, View):
    def get(self, request, slug, *arg, **kwargs):

        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        reviews = recipe.reviews.filter(
            approved=True).order_by('created_on')
        IngredientFormSet = inlineformset_factory(
            Recipe, RecipeIngredient, form=AddIngredientForm, extra=0)
        ingredient_formset = IngredientFormSet(instance=recipe)

        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        rated = False
        if recipe.rated_users.filter(id=request.user.id).exists():
            rated = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "reviews": reviews,
                "reviewed": False,
                "rated": rated,
                "liked": liked,
                'review_form': ReviewForm(),
                'recipe_form': RecipeForm(instance=recipe),
                "ingredient_formset": ingredient_formset,
            },
        )

    def post(self, request, slug, *arg, **kwargs):
        queryset = Recipe.objects.all()
        # queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        reviews = recipe.reviews.filter(approved=True).order_by('created_on')
        # ingredients = recipe.ingredients
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        rated = False
        if recipe.rated_users.filter(id=request.user.id).exists():
            rated = True

        review_form = ReviewForm(data=request.POST)

        # Create an instance of the inline formset for RecipeIngredient
        IngredientFormSet = inlineformset_factory(
            Recipe, RecipeIngredient, form=AddIngredientForm, extra=0)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)

        recipe_form = RecipeForm(data=request.POST, instance=recipe)

        if recipe_form.is_valid():
            rating_value = recipe_form.cleaned_data.get('rating')
            recipe.rate_recipe(request.user, rating_value)
            rating = recipe_form.save(commit=False)
            rating.recipe = recipe
            rating.save()
        else:
            recipe_form = RecipeForm()

        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review = review_form.save(commit=False)
            review.recipe = recipe
            review.save()

            messages.success(request, 'Review submitted successfully.')

            return redirect('recipe_images')
        else:
            review_form = ReviewForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "reviews": reviews,
                "reviewed": True,
                "rated": rated,
                "liked": liked,
                'review_form': ReviewForm(),
                'recipe_form': RecipeForm(instance=recipe),
                "ingredient_formset": ingredient_formset,
            },
        )


class RecipeLike(View):
    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class AddRecipeView(LoginRequiredMixin, FormView):
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'add_recipe.html'
    success_url = reverse_lazy('recipe_images')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.email = self.request.user.email
        form.instance.name = self.request.user.username
        self.formset = form.ingredient_formset
        # message for added recipe draft or published
        self.status = self.request.POST.get('status')
        if self.status == '0':
            messages.success(
                self.request,
                f'Recipe "{form.instance.title}" draft added successfully.'
            )
        else:
            messages.success(
                self.request,
                f'Recipe "{form.instance.title}" added successfully.'
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error in the form submission.'
            ' Please check the error field.'
        )
        print("Form or Formset is invalid")
        print("Form errors:", form.errors)
        print("Formset errors:", self.formset.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        print("Entering post method")
        form = self.get_form()
        self.formset = form.ingredient_formset

        if form.is_valid() and self.formset.is_valid():
            form.instance.author = self.request.user
            form.instance.email = self.request.user.email
            form.instance.name = self.request.user.username
            form.save()

            self.formset.instance = form.instance

            instances = self.formset.save(commit=False)

            for instance in instances:
                instance.recipe = form.instance
                instance.save()

            self.formset.save()

            return self.form_valid(form)
        else:
            print("Form is invalid")
            return self.form_invalid(form)


class UpdateRecipeView(LoginRequiredMixin, View):
    template_name = 'update_recipe.html'
    IngredientFormSet = inlineformset_factory(
        Recipe,
        RecipeIngredient,
        form=AddIngredientForm,
        extra=25,
        max_num=25,
    )

    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        # Check if the current user is the owner of the recipe
        if request.user != recipe.author:
            messages.error(
                request,
                "You don't have permission to update this recipe."
            )
            # Redirect to recipes for unauthorized access
            return redirect('recipe_images')
        update_recipe_form = UpdateRecipeForm(instance=recipe)
        ingredient_formset = self.IngredientFormSet(instance=recipe)

        image = recipe.featured_image

        return render(
            request,
            self.template_name,
            {
                'update_recipe_form': update_recipe_form,
                'ingredient_formset': ingredient_formset,
                'recipe': recipe,
                'image': image,
            }
        )

    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        # Check if the current user is the owner of the recipe
        if request.user != recipe.author:
            messages.error(
                request,
                "You don't have permission to update this recipe."
            )
            # Redirect to home page for unauthorized access
            return redirect('recipe_images')
        update_recipe_form = UpdateRecipeForm(
            request.POST,
            request.FILES,
            instance=recipe
        )
        ingredient_formset = self.IngredientFormSet(
                request.POST,
                instance=recipe,
                queryset=RecipeIngredient.objects.filter(recipe=recipe)
        )
        image = recipe.featured_image
        for form in ingredient_formset:
            form.fields['name'].widget.attrs['class'] = 'ingredient-name'
            form.fields['quantity'].widget.attrs['class'] = (
                'ingredient-quantity'
            )
            form.fields['unit'].widget.attrs['class'] = 'ingredient-unit'
            form.fields['DELETE'].required = False

        if update_recipe_form.is_valid() and ingredient_formset.is_valid():
            update_recipe_form.save()
            ingredient_formset.save()

            messages.success(
                request,
                f'Recipe "{recipe.title}" updated successfully.'
            )
            return redirect('recipe_images')

        else:
            return render(
                request,
                self.template_name,
                {
                    'update_recipe_form': update_recipe_form,
                    'ingredient_formset': ingredient_formset,
                    'recipe': recipe,
                    'image': image,
                }
            )


class DeleteRecipeView(LoginRequiredMixin, View):

    template_name = 'recipe_detail.html'

    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            messages.error(
                request,
                "You don't have permission to delete this recipe."
            )
            # Redirect to recipes page for unauthorized access
            return redirect('recipe_images')
        recipe_name = recipe.title
        recipe.delete()

        messages.success(
            request,
            f'Recipe "{recipe_name}" deleted successfully.'
        )

        return redirect('recipe_images')
