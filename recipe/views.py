from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import datetime
import markdown2

from django.contrib.auth.models import User
from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile
from . import measures

#
## Page requests
#

def index(request):
    return render(request, "recipe/home.html")

def mywine(request):
    return render(request, "recipe/mywine.html")

def recipes(request):
    return render(request, "recipe/recipes.html")

def newrecipe(request):
    if request.method == "GET":
        return render(request, "recipe/newrecipe.html", {'styles': list(WineStyle.objects.values())})

    # POST - create a new recipe from the form data then render recipe page
    data = {
        'id': -1,
        'name': request.POST.get("name"),
        'style_id': request.POST.get("style"),
        'volume_l': request.POST.get("volume"),
        'description': request.POST.get("descr"),
        'created_by': request.user
    }

    if request.user.is_authenticated:
        recipe = Recipe.objects.create(
            name=data['name'],
            style_id=data['style_id'],
            volume_l=data['volume_l'],
            description=data['description'],
            created_by=data['created_by']
            )
        data['id'] = recipe.id

    return render(request, "recipe/recipe.html", data )

def recipe(request):
    if request.method == "GET":
        id = int(request.GET.get("id"))
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

        data = {'id': id, 'name': recipe.name, 'volume_l': recipe.volume_l, 'descr': recipe.description}
        return render(request, "recipe/recipe.html", data )
    else:
        # Posted recipe form to save the recipe
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

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
            use, created = IngredientUse.objects.get_or_create(recipe_id=id, ingredient_id=ingredient_id, defaults={'qty_kg': 1.0,'order': 0})
            oldUses = oldUses.exclude(recipe_id=id, ingredient_id=ingredient_id)
            use.qty_kg = qty
            use.order = order
            use.save()

        # Remove old ingredient uses that are no longer used.
        oldUses.delete()
            
        # Recipe page updates itself so no need to return the recipe page 
        return HttpResponse("")

def newbrew(request):
    if request.user.is_anonymous:
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        # Getting the form to start a brew
        id = int(request.GET.get("recipe_id"))
        try:
            recipe = Recipe.objects.get(id=id).to_dict()
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

        return render(request, "recipe/newbrew.html", {'recipe': recipe, 'recipe_id': id} )

    else:
        # Posting details to start a brew
        id = int(request.POST.get("recipe_id"))
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

        # Create the new brew entry
        data = {
            'user': request.user,
            'recipe_id': request.POST.get('recipe_id'),
            'recipe_name': recipe.name,
            'size_l': request.POST.get('volume')
        }

        brew = Brew.objects.create(
                user=data['user'],
                recipe_id=data['recipe_id'],
                size_l=data['size_l']
                )
        data['id'] = brew.id

        return HttpResponseRedirect(f"/brew?id={brew.id}")

def brew(request):
    if request.method != "GET":
        return HttpResponse('The request is not valid.', status=400)

    id = int(request.GET.get("id"))
    try:
        brew = Brew.objects.get(id=id)
    except Recipe.DoesNotExist:
        raise Http404(f"Brew {id} does not exist")
    
    recipe = Recipe.objects.get(id=brew.recipe_id)
    data = {
        'brew': brew.to_dict(),
        'recipe': recipe.to_dict(),
        }
    return render(request, "recipe/brew.html", data )

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
    if request.user.is_anonymous:
        return HttpResponse('Unauthorized', status=401)

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


#
## API requests 
#

def apiRecipeList(request):
    order = request.GET.get("order")
    thisUserOnly = request.GET.get("thisUserOnly")
    recent = request.GET.get("recent")
    if thisUserOnly:
        recipelist = Recipe.objects.filter(created_by=request.user)
    else:
        recipelist = Recipe.objects.all()

    if recent:
        days = 7
        recentlist = []
        while len(recentlist) < 10 and days <= 448:
            recentlist = recipelist.filter(create_date__gte=datetime.date.today()-datetime.timedelta(days=days))
            days *= 2
        recipelist = recentlist

    arglist = order.split(',')
    recipes = list(recipelist.order_by(*arglist).values())
    for recipe in recipes:
        try:
            recipe['style'] = WineStyle.objects.filter(id=recipe['style_id']).values()[0]
            recipe['created_by'] = User.objects.filter(id=recipe['created_by_id']).values()[0]['username']
        except:
            pass
    return JsonResponse({'recipes': recipes}, safe=False)

def apiRecipe(request):
    id = int(request.GET.get("id"))
    if id < 0:
        recipe = {'id': -1, 'name': '', 'volume': 0, 'descr': '', 'ingredients': [] }
    else:
        recipe = Recipe.objects.get(id=id).to_dict()

    data = { 
        'recipe': recipe,
        'ingredients': list(Ingredient.objects.order_by('name','variety').values()),
        'styles': list(WineStyle.objects.values()),
        'methods': list(Method.objects.values()),
        'liquid': {'units': list(measures.Liquid.UNITS), 'conv': list(measures.Liquid.CONV)},
        'solid': {'units': list(measures.Solid.UNITS), 'conv': list(measures.Solid.CONV)},
    }

    if request.user.is_authenticated:
        data['profile'] = Profile.objects.filter(user=request.user).values()[0]
    else:
        data['profile'] = None

    return JsonResponse(data, safe=False)

def apiBrewList(request):
    order = request.GET.get("order")
    recent = request.GET.get("recent")
    thisUserOnly = request.GET.get("thisUserOnly")
    if thisUserOnly:
        brewlist = Brew.objects.filter(user=request.user)
    else:
        brewlist = Brew.objects.all()

    if recent:
        days = 7
        recentlist = []
        while len(recentlist) < 10 and days <= 448:
            recentlist = brewlist.filter(updated__gte=datetime.date.today()-datetime.timedelta(days=days))
            days *= 2
        brewlist = recentlist

    arglist = order.split(',')
    brews = list(brewlist.order_by(*arglist).values())
    for brew in brews:
        try:
            brew['user'] = User.objects.filter(id=brew['user_id']).values()[0]['username']
            brew['recipe'] = Recipe.objects.get(id=brew['recipe_id']).to_dict()
            brew['recipe']['style'] = WineStyle.objects.filter(id=brew['recipe']['style']).values()[0]
        except:
            pass
    return JsonResponse({'brews': brews}, safe=False)

def apiBrewLog(request):
    if request.method == "GET":
        id = int(request.GET.get("id"))
        try:
            brew = Brew.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404(f"Brew {id} does not exist")

    else:
        # Posting a log entry
        if request.user.is_anonymous:
            return HttpResponse('You must be logged in to add logs.', status=401)

        id = int(request.POST.get("id"))
        try:
            brew = Brew.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404(f"Brew {id} does not exist")

        # Is the user authorised to add a log entry to this brew?
        if not request.user.is_superuser and request.user != brew.user:
            return HttpResponse("You are not nauthorized to add a log entry to this brew.", status=401)

        LogEntry.objects.create(
            datetime = datetime.datetime.now(),
            text = request.POST.get('logtext'),
            brew_id = id,
            user = request.user
        )

    return getLog(brew)

def apiBrewComment(request):
    if request.user.is_anonymous:
        return HttpResponse('You must be logged in to add comments.', status=401)

    if request.method == "GET":
        return HttpResponse('The request is not valid.', status=400)

    logEntry_id = int(request.POST.get("logEntry_id"))
    try:
        logEntry = LogEntry.objects.get(id=logEntry_id)
    except LogEntry.DoesNotExist:
        raise Http404(f"LogEntry {id} does not exist")

    Comment.objects.create(
        datetime = datetime.datetime.now(),
        text = request.POST.get('comment'),
        brew_id = logEntry.brew_id,
        logEntry_id = logEntry_id,
        user = request.user
    )

    return getLog(Brew.objects.get(id=logEntry.brew_id)
)

def getLog(brew):
    # Return all log entries and comments for this brew
    log = list(LogEntry.objects.filter(brew=brew).values())
    htmlLog = []
    for logEntry in log:
        try:
            logEntry['user'] = User.objects.filter(id=logEntry['user_id']).values()[0]['username']
        except:
            pass
        comments = list(Comment.objects.filter(logEntry_id=logEntry['id']).values())
        logEntry['comments'] = []
        for comment in comments:
            try:
                comment['user'] = User.objects.filter(id=comment['user_id']).values()[0]['username']
            except:
                pass
            logEntry['comments'].append(comment)

    return JsonResponse({'log': log}, safe=False)