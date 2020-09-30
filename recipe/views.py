from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import datetime

from django.contrib.auth.models import User
from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile
from . import measures

''' Index page.
    GET, No parameters
'''
def index(request):
    return render(request, "recipe/home.html")

''' MyWine page.
    GET:
        No parameters
'''
def mywine(request):
    return render(request, "recipe/mywine.html")

''' Recipes page.
    GET:
        No parameters
'''
def recipes(request):
    return render(request, "recipe/recipes.html")

''' New recipe page.
    GET: Gets the new recipe form.
        No parameters

    POST: Posts the new recipe form and returns a recipe page containing the new
    recipe.
        name        the recipe name
        style       the ID of the wines style chosen by the dropdown
        volume      the wine recipe volume (L)
        descr       an optionally blank description
'''
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

''' Recipe page
    GET: get a recipe page
        id:         the recipe ID

    POST: post the (modified) recipe data to store it in the recipe
        name        the recipe name
        volume      the wine recipe volume (L)
        descr       an optionally blank description
        ingredient_id[]     list of ingredient IDs for each ingredient
        ingredient_order[]  list of sort order for each ingredient
        qty[]               list of quantities (kg solid, L liquid) for each ingredient
'''
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

''' New brew page.
    GET: Gets the new brew form.
        No parameters

    POST: Posts the new brew form and returns a brew page containing the new
    brew.
        recipe_id   the ID of the recipe to brew
        volume      the wine recipe volume (L)
'''
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

''' Brew page
    GET: get a brew page
        id:         the brew ID
'''
def brew(request):
    if request.method != "GET":
        return HttpResponse('The request is not valid.', status=400)

    id = int(request.GET.get("id"))
    try:
        brew = Brew.objects.get(id=id)
    except Brew.DoesNotExist:
        raise Http404(f"Brew {id} does not exist")
    
    recipe = Recipe.objects.get(id=brew.recipe_id)
    tab = request.GET.get("tab", "")
    data = {
        'brew': brew.to_dict(),
        'recipe': recipe.to_dict(),
        'tab': tab,
        'canModify': canModifyBrew(request.user, brew),
        }
    return render(request, "recipe/brew.html", data )

''' User registration page
    GET: get the user registration form
        No parameters

    POST: post the form to create a user
'''
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

''' User profile page
    GET: get the current user's profile
        No parameters.

    POST: post the modified user's profile
        first_name
        last_name
        location
        solid_small_units
        solid_large_units
        liquid_small_units
        liquid_large_units
'''
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


''' API Get a list of recipes.
    GET:
        order           list of fields to set the sort order. It is a comma with
                        no white-space separated list. Each field name must by in
                        the form required by the order_by() Django QuerySet method
        thisUserOnly    if True then only recipes belonging to this user are returned
        recent          if True then only the most recent recipes are returned and 
                        parameter order is ignored
    
        Returns a JSON list of recipes. Each recipe has
            all the fields from the recipe record, plus
            style       all the fields of the style set for the recipe
            create_by   the username of the person that created the recipe
'''
def apiRecipeList(request):
    order = request.GET.get("order")
    thisUserOnly = request.GET.get("thisUserOnly")
    recent = request.GET.get("recent")
    if thisUserOnly:
        recipelist = Recipe.objects.filter(created_by=request.user)
    else:
        recipelist = Recipe.objects.all()

    if recent:
        recipes = list(recipelist.order_by('-create_date')[0:10].values())
    else:
        arglist = order.split(',')
        recipes = list(recipelist.order_by(*arglist).values())

    for recipe in recipes:
        styles = WineStyle.objects.filter(id=recipe['style_id'])
        recipe['style'] = styles.values()[0] if styles else None
        users = User.objects.filter(id=recipe['created_by_id'])
        recipe['created_by'] = users.values()[0]['username'] if users else None

    return JsonResponse({'recipes': recipes}, safe=False)

''' API Get the full details for a recipe.
    GET:
        id          the ID of the required recipe

        Returns JSON containing
            recipe      all the fields from the recipe record
            ingredients an alphabetically ordered list of records for all possible ingredients
            styles      an list of records for all possible wine style
            methods     an list of records for all possible preparation methods
            liquid      
                units   a list of liquid units
                conv    a list containing conversion factor for each unit
                step    a list containing spinner step for each unit
                decimals    a list containing deciaml places to display for each unit
            solid       lists of solid units, like the liquid lists
'''
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
        'liquid': {
            'units': list(measures.Liquid.UNITS),
            'conv': list(measures.Liquid.CONV),
            'step': list(measures.Liquid.STEP),
            'decimals': list(measures.Liquid.DECIMALS),
        },
        'solid': {
            'units': list(measures.Solid.UNITS),
            'conv': list(measures.Solid.CONV),
            'step': list(measures.Solid.STEP),
            'decimals': list(measures.Solid.DECIMALS),
        },
    }

    if request.user.is_authenticated:
        data['profile'] = Profile.objects.filter(user=request.user).values()[0]
    else:
        data['profile'] = None

    return JsonResponse(data, safe=False)

''' API Get a list of brews.
    GET:
        parameters are the same as apiRecipeList()
    
        Returns a JSON list of brews. Each brew has
            all the fields from the brew record, plus
            user        the username of the person who owns the brew
            recipe      all the fields of the recipe used for the brew plus
                style       all the fields of the style set for the recipe
'''
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

''' API Get or set log entries for a brew.
    GET:
        id          the ID of the brew to get

        Returns in JSON format a chronological list of log entries for the brew
        Each log entry contains the log entry data plus
            user        the username of the user that made the log entry
            comments    a chronological list of comments attached to the log entry

    POST: new log entry
        brew_id     the ID of the brew being logged
        logtext     the text for the log

        Returns the same as GET.

    POST: modify log entry
        logEntry_id the ID of the log entry to be modified
        logtext     the replacement text for the log entry

        Returns the same as GET.
'''
def apiBrewLog(request):
    if request.method == "GET":
        brew_id = int(request.GET.get("brew_id"))
        try:
            brew = Brew.objects.get(id=brew_id)
        except Recipe.DoesNotExist:
            raise Http404(f"Brew {brew_id} does not exist")

    else:
        # Posting a log entry
        if request.user.is_anonymous:
            return HttpResponse('You must be logged in to add logs.', status=401)

        brew_id = request.POST.get("brew_id")
        logEntry_id = request.POST.get("logEntry_id")
        if brew_id:
            try:
                brew = Brew.objects.get(id=int(brew_id))
            except Brew.DoesNotExist:
                raise Http404(f"Brew {brew_id} does not exist")

            # Is the user authorised to add a log entry to this brew?
            if not canModifyBrew(request.user, brew):
                return HttpResponse("You are not nauthorized to add a log entry to this brew.", status=401)

            LogEntry.objects.create(
                datetime = datetime.datetime.now(),
                text = request.POST.get('logtext').rstrip(" \t\r\n"),
                brew_id = brew_id,
                user = request.user
            )

            brew.log_count = LogEntry.objects.filter(brew_id=brew_id).count()
            brew.updated = datetime.datetime.now()
            brew.save()

        elif logEntry_id:
            try:
                logEntry = LogEntry.objects.get(id=int(logEntry_id))
            except LogEntry.DoesNotExist:
                raise Http404(f"Log entry {logEntry_id} does not exist")

            # Is the user authorised to edit a log entry to this brew?
            if not canModifyBrew(request.user, logEntry.brew):
                return HttpResponse("You are not authorized to add a log entry to this brew.", status=401)

            logEntry.text = request.POST.get('logtext').rstrip(" \t\r\n")
            logEntry.user = request.user
            logEntry.save()
            brew = logEntry.brew
            brew.log_count = LogEntry.objects.filter(brew_id=brew.id).count()
            brew.updated = datetime.datetime.now()
            brew.save()

        else:
            return HttpResponse("Request must contain brew_id or logEntry_id", status=400)

    return getLog(brew)

''' API Delete a brew log entry
    POST:
        logEntry_id     the ID of the log entry to be deleted

        Returns same as apiBrewLog().
'''
def apiBrewLogDelete(request):
    # Posting to delete a log entry
    if request.user.is_anonymous:
        return HttpResponse('You must be logged in to delete logs.', status=401)

    logEntry_id = request.POST.get("logEntry_id")
    if logEntry_id:
        try:
            logEntry = LogEntry.objects.get(id=int(logEntry_id))
        except LogEntry.DoesNotExist:
            raise Http404(f"Log entry {logEntry_id} does not exist")

        # Is the user authorised to edit a log entry to this brew?
        if not canModifyBrew(request.user, logEntry.brew):
            return HttpResponse("You are not authorized to delete a log entry in this brew.", status=401)

        brew = logEntry.brew
        logEntry.delete()
        brew.log_count = LogEntry.objects.filter(brew_id=brew.id).count()
        brew.updated = datetime.datetime.now()
        brew.save()

    else:
        return HttpResponse("Request must contain logEntry_id", status=400)

    return getLog(brew)

''' API Add a comment to a brew.
    POST:
        logEntry_id     the ID of the log entry that the comment is for
        comment         the text of the comment

        Returns same as apiBrewLog().
'''
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
        text = request.POST.get('comment').rstrip(" \t\r\n"),
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

def canModifyBrew(user, brew):
    return user.is_superuser or user == brew.user

def canModifyRecipe(user, recipe):
    return user.is_superuser or user == recipe.created_by
