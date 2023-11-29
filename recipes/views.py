from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .models import Recipe, Review, RecipeIngredient
from .forms import ReviewForm, RecipeForm, AddRecipeForm


# Create your views here.
class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class RecipeDetails(View):
    def get(self, request, slug, *arg, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        reviews = recipe.reviews.filter(approved=True).order_by('created_on')
        ingredients = recipe.ingredients
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
                "ingredients": ingredients,
                'review_form': ReviewForm(),
                'recipe_form': RecipeForm(instance=recipe),
            },
        )
    
    def post(self, request, slug, *arg, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        reviews = recipe.reviews.filter(approved=True).order_by('created_on')
        ingredients = recipe.ingredients
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        rated = False
        if recipe.rated_users.filter(id=request.user.id).exists():
            rated = True

        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review = review_form.save(commit=False)
            review.recipe = recipe
            review.save()
        else:
            review_form = ReviewForm()
      
        recipe_form = RecipeForm(data=request.POST, instance=recipe)

        if recipe_form.is_valid():
            rating_value = recipe_form.cleaned_data.get('rating')
            recipe.rate_recipe(request.user.id, rating_value)
            rating = recipe_form.save(commit=False)
            rating.recipe = recipe
            rating.save()
        else:
            recipe_form = RecipeForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "reviews": reviews,
                "reviewed": True,
                "rated": rated,
                "liked": liked,
                "ingredients": ingredients,
                'review_form': ReviewForm(),
                'recipe_form': RecipeForm(instance=recipe),
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


class AddRecipeView(FormView):
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'add_recipe.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.email = self.request.user.email
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        print("Entering post method")
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.email = self.request.user.email
            form.instance.name = self.request.user.username
            form.save()
            return self.form_valid(form)
        else:
            print("Form is invalid")
            return self.form_invalid(form)

    