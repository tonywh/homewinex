from django.test import TestCase, Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile

class PagesTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username="user1", password="user1_pw")
        admin = User.objects.create_user(username="admin", password="admin_pw")
        admin.is_superuser = True
        admin.save()

        # Create recipes
        # Create Brews
        # Create brew logs and comments
        pass

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_mywine(self):
        c = Client()
        response = c.get("/mywine")
        self.assertEqual(response.status_code, 200)

    def test_recipe(self):
        c = Client()
        response = c.get("/recipes")
        self.assertEqual(response.status_code, 200)

    def test_new_recipe_get(self):
        c = Client()
        response = c.get("/newrecipe")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context['styles']), 10)

    def test_new_recipe_post_anonymous(self):
        c = Client()
        num_recipes = Recipe.objects.all().count()
        data = {
            'name': 'recipe X',
            'style': WineStyle.objects.first().id,
            'volume': 5.0,
            'descr': 'great wine',
        }
        response = c.post("/newrecipe", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name'], data['name'])
        self.assertEqual(int(response.context['style_id']), data['style'])
        self.assertEqual(float(response.context['volume_l']), data['volume'])
        self.assertEqual(response.context['description'], data['descr'])
        self.assertEqual(num_recipes, Recipe.objects.all().count())

    def test_new_recipe_post_authenticated(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        num_recipes = Recipe.objects.all().count()
        data = {
            'name': 'recipe X',
            'style': WineStyle.objects.first().id,
            'volume': 5.0,
            'descr': 'great wine',
        }
        response = c.post("/newrecipe", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name'], data['name'])
        self.assertEqual(int(response.context['style_id']), data['style'])
        self.assertEqual(float(response.context['volume_l']), data['volume'])
        self.assertEqual(response.context['description'], data['descr'])
        self.assertEqual(num_recipes + 1, Recipe.objects.all().count())
        recipe = Recipe.objects.get(id=response.context['id'])
        self.assertEqual(recipe.name, data['name'])
        self.assertEqual(recipe.style_id, data['style'])
        self.assertEqual(recipe.volume_l, data['volume'])
        self.assertEqual(recipe.description, data['descr'])
