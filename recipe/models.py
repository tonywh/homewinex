from django.db import models
from django.contrib.auth.models import User
from itertools import chain
from . import measures

class Method(models.Model):
    method_num = models.IntegerField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.method_num}: {self.description}"

class Ingredient(models.Model):
    ''' All proportions are stored as g/l or g/kg 
    '''
    name = models.CharField(max_length=128)
    variety = models.CharField(max_length=128)
    acid = models.FloatField()          # as tartaric
    sugar = models.FloatField()
    unferm_sugar = models.FloatField()
    solu_solid = models.FloatField()
    body_to_acid = models.FloatField()  # solu_solid / acid
    tannin = models.FloatField()
    pectin = models.BooleanField()
    pectolaise = models.BooleanField()
    redness = models.FloatField()       # scale 1 - 10
    brownness = models.FloatField()     # scale 1 - 10
    starch = models.FloatField()
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    liquid = models.FloatField()        # 1000.0 means it's a liquid ingredient
    suggest_max = models.FloatField()   # max suggested quantity of the ingredient

    class Meta:
        ordering = ['name', 'variety']

    def __str__(self):
        return f"{self.name}, {self.variety}"

class WineStyle(models.Model):
    ''' All proportions are stored as g/l, except alcohol which is % vol.
    '''
    sweetness = models.CharField(max_length=32)
    colour = models.CharField(max_length=32)
    grapes = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    alcohol = models.FloatField()
    acid = models.FloatField()
    tannin = models.FloatField()
    solu_solid = models.FloatField()

    class Meta:
        ordering = ['grapes', 'region']

    def __str__(self):
        return f"{self.grapes}, {self.region}"

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientUse', related_name='recipes')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateField()
    volume_l = models.FloatField()
    description = models.TextField()
    style = models.ForeignKey(WineStyle, on_delete=models.PROTECT)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.id}: {self.name}"

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)

        ingredientuses = list(IngredientUse.objects.filter(recipe_id=self.id).values())
        print(ingredientuses)
        data['ingredients'] = ingredientuses
        return data

class IngredientUse(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    qty_kg = models.FloatField()

class Brew(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    size_l = models.FloatField()
    image = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.recipe}, {self.user}"

class LogEntry(models.Model):
    datetime = models.DateField()
    text = models.TextField()
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)

class Image(models.Model):
    location = models.FileField()
    parent = models.ForeignKey(LogEntry, on_delete=models.CASCADE, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True, default='')
    solid_small_units = models.PositiveSmallIntegerField(choices=measures.Solid.UNITS, default=measures.Solid.G)
    solid_large_units = models.PositiveSmallIntegerField(choices=measures.Solid.UNITS, default=measures.Solid.KG)
    liquid_small_units = models.PositiveSmallIntegerField(choices=measures.Liquid.UNITS, default=measures.Liquid.ML)
    liquid_large_units = models.PositiveSmallIntegerField(choices=measures.Liquid.UNITS, default=measures.Liquid.L)

    def __str__(self):
        return self.user.username