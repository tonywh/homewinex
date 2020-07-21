from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes", views.recipes, name="recipes"),
    path("mywine", views.mywine, name="mywine"),
    path("recipelist", views.recipelist, name="recipelist"),
    path("newrecipe", views.newrecipe, name="newrecipe"),
    path("recipe", views.recipe, name="recipe"),
    path("newbrew", views.newbrew, name="newbrew"),
    path("brew", views.brew, name="brew"),
    path("recipedetail", views.recipedetail, name="recipedetail"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register", views.register, name="register"),
    path("accounts/profile", views.profile, name="profile"),
]