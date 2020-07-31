from django.urls import path, include

from . import views

urlpatterns = [
    # Pages
    path("", views.index, name="index"),
    path("recipes", views.recipes, name="recipes"),
    path("mywine", views.mywine, name="mywine"),
    path("newrecipe", views.newrecipe, name="newrecipe"),
    path("recipe", views.recipe, name="recipe"),
    path("newbrew", views.newbrew, name="newbrew"),
    path("brew", views.brew, name="brew"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register", views.register, name="register"),
    path("accounts/profile", views.profile, name="profile"),

    # APIs
    path("api/recipelist", views.apiRecipeList, name="apiRecipeList"),
    path("api/recipe", views.apiRecipe, name="apiRecipe"),
    path("api/brewlog", views.apiBrewLog, name="apiBrewLog"),
    path("api/brewcomment", views.apiBrewComment, name="apiBrewComment"),
]