from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from datetime import datetime

from .models import Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image, WineStyle, Profile

def index(request):
    return HttpResponseRedirect("/recipes")

def recipes(request):
    return render(request, "recipe/recipes.html", data )

def recipe(request):
    id = int(request.GET.get("id"))
    if id < 0:
        # Creating a new recipe from Get request, e.g.
        #/recipe?id=-1&name=MyWine&volume=25&descr=This%20is%20my%20new%20wine%20recipe.
        data = {'id': -1, 'name': request.GET.get("name"), 'volume': request.GET.get("volume"), 'descr': request.GET.get("descr")}
    else:
        recipe = Recipe.objects.get(id=id)
        data = {'id': id, 'name': recipe.name, 'volume': recipe.volume_l, 'descr': recipe.description}

    return render(request, "recipe/recipe.html", data )

def recipedetail(request):
    id = int(request.GET.get("id"))
    if id < 0:
        recipe = {'id': -1, 'name': '', 'volume': 0, 'descr': '', 'ingredients': [] }
    else:
        recipe = Recipe.objects.get(id=id).to_dict()
    
    data = { 
        'recipe': recipe,
        'ingredients': list(Ingredient.objects.order_by('name','variety').values()),
        'styles': list(WineStyle.objects.values()),
    }
    return JsonResponse(data, safe=False)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=user)
            return HttpResponseRedirect("/accounts/profile")

    form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})

def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        profile.location = request.POST.get('location')
        profile.solid_small_units = request.POST.get('solid_small_units')
        profile.solid_large_units = request.POST.get('solid_large_units')
        profile.liquid_small_units = request.POST.get('liquid_small_units')
        profile.liquid_large_units = request.POST.get('liquid_large_units')
        profile.save()
        profile = Profile.objects.get(user=user)

    return render(request, "recipe/profile.html", {'user': user, 'profile': profile})
