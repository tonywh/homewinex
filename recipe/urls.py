from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes", views.recipes, name="recipes"),
    path("newrecipe", views.newrecipe, name="newrecipe"),
    path("recipe", views.recipe, name="recipe"),
    path("recipedetail", views.recipedetail, name="recipedetail"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register", views.register, name="register"),
    path("accounts/profile", views.profile, name="profile"),
]