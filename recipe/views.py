from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import datetime

from django.contrib.auth.models import User
from .models import Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image, WineStyle, Profile

def index(request):
    return HttpResponseRedirect("/recipes")

def recipes(request):
    return render(request, "recipe/recipes.html")

def recipelist(request):
    order = request.GET.get("order")
    arglist = order.split(',')
    recipes = list(Recipe.objects.all().order_by(*arglist).values())
    for recipe in recipes:
        try:
            recipe['style'] = WineStyle.objects.filter(id=recipe['style_id']).values()[0]
            recipe['created_by'] = User.objects.filter(id=recipe['created_by_id']).values()[0]
        except:
            pass
    return JsonResponse({'recipes': recipes}, safe=False)

def newrecipe(request):
    if request.method == "GET":
        return render(request, "recipe/newrecipe.html", {'styles': list(WineStyle.objects.values())})

    # POST - create a new recipe from the form data then render recipe page
    print(request.POST.get("name"))
    print(request.POST.get("style"))
    print(request.POST.get("volume"))

    recipe = Recipe.objects.create(
        name=request.POST.get("name"),
        style_id=request.POST.get("style"),
        volume_l=request.POST.get("volume"),
        description=request.POST.get("descr"),
        created_by=request.user
        )

    data = {'id': recipe.id, 'name': recipe.name, 'volume': recipe.volume_l, 'descr': recipe.description}
    return render(request, "recipe/recipe.html", data )

def recipe(request):
    if request.method == "GET":
        id = int(request.GET.get("id"))
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

        data = {'id': id, 'name': recipe.name, 'volume': recipe.volume_l, 'descr': recipe.description}
        return render(request, "recipe/recipe.html", data )
    else:
        print(request.POST)
        id = int(request.POST.get("id"))
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

        recipe.name = request.POST.get("name")
        recipe.volume = request.POST.get("volume")
        recipe.description = request.POST.get("descr")
        ingredient_ids = request.POST.getlist("ingredient_id[]")
        orders = request.POST.getlist("ingredient_order[]")
        qtys = request.POST.getlist("qty[]")
        oldUses = IngredientUse.objects.filter(recipe_id=id)

        # Update / add ingredient uses.
        for ingredient_id, qty, order in zip(ingredient_ids, qtys, orders):
            use, created = IngredientUse.objects.get_or_create(recipe_id=id, ingredient_id=ingredient_id, defaults={'qty_kg': 1.0})
            oldUses = oldUses.exclude(recipe_id=id, ingredient_id=ingredient_id)
            use.qty_kg = qty
            use.order = order
            use.save()

        # Remove old ingredient uses that are no longer used.
        oldUses.delete()
            
        return HttpResponse("")

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
