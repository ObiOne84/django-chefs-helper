from django.contrib import admin
from .models import Recipe, Review, RecipeIngredient
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    summernote_fields = ('instructions')


# Register your models here.
# admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(RecipeIngredient)