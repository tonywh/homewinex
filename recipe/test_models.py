from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile

class WineStyleTestCase(TestCase):

    def setUp(self):
        pass

    def test_winestyle_ordering(self):
        laststyle = None
        for style in WineStyle.objects.values():
            if laststyle != None:
                self.assertGreaterEqual(style.grapes,laststyle.grapes)
                if style.grapes == laststyle.grapes:
                    self.assertGreaterEqual(style.region,laststyle.region)

class RecipeAndIngredientTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="user1", password="user1_pw")
        ingredients = Ingredient.objects.all()
        styles = WineStyle.objects.all()
        recipe = Recipe.objects.create( name='a', style=styles[0], volume_l=5, description='', created_by=user)
        IngredientUse.objects.create(ingredient=ingredients[0],recipe=recipe,qty_kg=1.0,order=1)
        IngredientUse.objects.create(ingredient=ingredients[1],recipe=recipe,qty_kg=2.0,order=0)

    def test_ingredient_use_ordering(self):
        recipe = Recipe.objects.get(name='a')
        lastuse = None
        for use in IngredientUse.objects.filter(recipe_id=recipe.id):
            if lastuse != None:
                self.assertGreaterEqual(use.order,lastuse.order)

    def test_recipe_to_dict(self):
        recipe = Recipe.objects.get(name='a')
        recipe_dict = recipe.to_dict()
        self.assertEqual(recipe_dict['name'],recipe.name)
        self.assertEqual(recipe_dict['ingredients'],list(IngredientUse.objects.filter(recipe_id=recipe.id).values()))
        self.assertEqual(recipe_dict['created_by'],recipe.created_by.username)
        self.assertEqual(recipe_dict['create_date'],date.today())
        self.assertEqual(recipe_dict['volume_l'],recipe.volume_l)
        self.assertEqual(recipe_dict['description'],recipe.description)
        self.assertEqual(recipe_dict['style'],recipe.style.id)
        self.assertEqual(recipe_dict['image'],recipe.image)

class BrewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="user1", password="user1_pw")
        ingredients = Ingredient.objects.all()
        styles = WineStyle.objects.all()
        recipe = Recipe.objects.create( name='a', style=styles[0], volume_l=5, description='', created_by=user)
        brew = Brew.objects.create(user=user,recipe=recipe,size_l=5.0)
        LogEntry.objects.create(datetime=datetime.now()+timedelta(days=1), text="2nd", brew=brew, user=user)
        log1 = LogEntry.objects.create(datetime=datetime.now(), text="1st", brew=brew, user=user)
        Comment.objects.create(datetime=datetime.now()+timedelta(days=2), text="2nd", brew=brew, logEntry=log1, user=user)
        Comment.objects.create(datetime=datetime.now(), text="1st", brew=brew, logEntry=log1, user=user)

    def test_brew_to_dict(self):
        user = User.objects.get(username="user1")
        brew = Brew.objects.get(user=user)
        brew_dict = brew.to_dict()
        self.assertEqual(brew_dict['id'],brew.id)
        self.assertEqual(brew_dict['user'],brew.user.username)
        self.assertEqual(brew_dict['recipe_id'],brew.recipe_id)
        self.assertEqual(brew_dict['size_l'],brew.size_l)
        self.assertEqual(brew_dict['image'],brew.image)

    def test_log_ordering(self):
        user = User.objects.get(username="user1")
        brew = Brew.objects.get(user=user)
        lastlog = None
        for log in LogEntry.objects.filter(brew=brew):
            if lastlog != None:
                self.assertGreaterEqual(log.datetime,lastlog.datetime)

    def test_comment_ordering(self):
        user = User.objects.get(username="user1")
        brew = Brew.objects.get(user=user)
        lastcomment = None
        for comment in Comment.objects.filter(brew=brew):
            if lastcomment != None:
                self.assertGreaterEqual(comment.datetime,lastcomment.datetime)

