from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Method, Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image, WineStyle, Profile

class IngredientUseInline(admin.TabularInline):
    model = IngredientUse
    extra = 1

class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngredientUseInline,)
    fields = ( ('name', 'variety'),
               ('acid', 'sugar', 'unferm_sugar', 'solu_solid', 'body_to_acid', 'tannin', 'starch', 'liquid'),
               ('pectin', 'pectolaise', 'redness', 'brownness', 'suggest_max'),
               ('method') )

class RecipeAdmin(admin.ModelAdmin):
#    filter_horizontal = ("ingredients",)
    inlines = (IngredientUseInline,)
    fields = ( ('name', 'volume_l', 'created_by', 'create_date'),
               ('style', 'visibility'),
               ( 'description', 'image' ) )

admin.site.register(Method)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientUse)
admin.site.register(Brew)
admin.site.register(LogEntry)
admin.site.register(Image)
admin.site.register(WineStyle)
admin.site.register(Profile)