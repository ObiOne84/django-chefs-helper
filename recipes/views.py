from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Recipe, Review, RecipeIngredient
from .forms import ReviewForm


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
        
        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "reviews": reviews,
                "liked": liked,
                "ingredients": ingredients,
                'review_form': ReviewForm(),
            },
        )








    