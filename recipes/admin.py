from django.contrib import admin
from .models import Recipe, Review, RecipeIngredient
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on', 'updated_on')
    search_fields = ['title']
    summernote_fields = ('instructions')
    actions = ['change_to_published']

    def change_to_published(self, request, queryset):
        queryset.update(status=1)


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    summernote_fields = ('body')
    list_display = ('name', 'recipe', 'body', 'created_on', 'approved')
    list_filter = ('created_on', 'approved')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'quantity', 'unit')
    search_fields = ['name']
