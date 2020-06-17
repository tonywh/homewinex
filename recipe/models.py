from django.db import models
from django.contrib.auth.models import User

class Method(models.Model):
    method_num = models.IntegerField(unique=True)
    description = models.TextField()

class Ingredient(models.Model):
    ''' All proportions are stored as g/l or g/kg 
    '''
    name = models.CharField(max_length=128)
    variety = models.CharField(max_length=128)
    acid = models.FloatField()          # as tartaric
    sugar = models.FloatField()
    unferm_sugar = models.FloatField()
    solu_solid = models.FloatField()
    body_to_acid = models.FloatField()  # don't know what this is
    tannin = models.FloatField()
    pectin = models.BooleanField()
    pectolaise = models.BooleanField()
    redness = models.FloatField()       # scale 1 - 10
    brownness = models.FloatField()     # scale 1 - 10
    starch = models.FloatField()
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    liquid = models.FloatField()        # 1000.0 means it's a liquid ingredient
    suggest_max = models.FloatField()   # max suggested quantity of the ingredient

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
