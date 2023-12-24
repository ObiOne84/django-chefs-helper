from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeImages.as_view(), name='home'),
    path(
        'add_recipe',
        views.AddRecipeView.as_view(),
        name='add_recipe'
    ),
    path(
        'like/<slug:slug>/',
        views.RecipeLike.as_view(),
        name='recipe_like'
    ),
    path(
        'recipe_images/',
        views.RecipeList.as_view(),
        name='recipe_images'
    ),
    path(
        '<slug:slug>/',
        views.RecipeDetails.as_view(),
        name='recipe_detail'
    ),
    path(
        'update_recipe/<slug:slug>/',
        views.UpdateRecipeView.as_view(),
        name='update_recipe'
    ),
    path(
        'delete/<slug:slug>/',
        views.DeleteRecipeView.as_view(),
        name='delete',
    ),
]
