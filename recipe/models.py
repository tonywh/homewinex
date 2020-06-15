from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    sg = models.FloatField()
    ta = models.FloatField()          # g/l as Tartaric
    tannin = models.FloatField()      # g/l
    yield_l = models.FloatField()     # l/kg. 1.0 means it's a liquid ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientUse')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateField()
    # add image here

class IngredientUse(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    qty_kg = models.FloatField()

class Brew(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    size_l = models.FloatField()
    # add image here

class LogEntry(models.Model):
    datetime = models.DateField()
    text = models.TextField()
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)

class Image:
    location = models.FileField()
    parent = models.ForeignKey(LogEntry, on_delete=models.CASCADE)
