from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Method, Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image, WineStyle, Profile

admin.site.register(Method)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientUse)
admin.site.register(Brew)
admin.site.register(LogEntry)
admin.site.register(Image)
admin.site.register(WineStyle)
admin.site.register(Profile)