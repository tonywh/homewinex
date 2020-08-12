from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import User
import nested_admin

from .models import Method, Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image, WineStyle, Profile, Comment

class IngredientUseInline(admin.TabularInline):
    model = IngredientUse
    extra = 0

class BrewInline(admin.TabularInline):
    model = Brew
    extra = 0

class CommentInline(nested_admin.NestedStackedInline):
    model = Comment
    extra = 0

class LogEntryInline(nested_admin.NestedStackedInline):
    model = LogEntry
    extra = 0
    inlines = [CommentInline]

class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngredientUseInline,)
    readonly_fields = ('id',)
    fields = ( ('id',),
               ('name', 'variety'),
               ('acid', 'sugar', 'unferm_sugar', 'solu_solid', 'body_to_acid', 'tannin', 'starch', 'liquid'),
               ('pectin', 'pectolaise', 'redness', 'brownness', 'suggest_max', 'default_qty_kg_per_l'),
               ('method') )

class RecipeAdmin(admin.ModelAdmin):
#    filter_horizontal = ("ingredients",)
    inlines = (IngredientUseInline,BrewInline)
    readonly_fields = ('id',)
    fields = ( ('id',),
               ('name', 'volume_l', 'created_by', 'create_date'),
               ('style', 'visibility'),
               ( 'description', 'image' ) )

class BrewAdmin(nested_admin.NestedModelAdmin):
    inlines = [LogEntryInline]
    fields = ( ('recipe', 'size_l', 'started', 'updated'), )

admin.site.register(Method)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Brew, BrewAdmin)
admin.site.register(WineStyle)
admin.site.register(Profile)