from django.test import TestCase, Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile

class PagesTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1_pw")
        profile1 = Profile.objects.create(user=user1)
        admin = User.objects.create_user(username="admin", password="admin_pw")
        profile2 = Profile.objects.create(user=admin)
        admin.is_superuser = True
        admin.save()

        self.recipe1 = Recipe.objects.create(name='recipe1', style_id=1, volume_l=5.0, created_by=user1)
        self.brew1 = Brew.objects.create(user=user1, recipe=self.recipe1,size_l=25.0)

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_mywine(self):
        c = Client()
        response = c.get("/mywine")
        self.assertEqual(response.status_code, 200)

    def test_recipes(self):
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

    def test_recipe_get_bad_id(self):
        c = Client()
        response = c.get("/recipe?id=100")
        self.assertEqual(response.status_code, 404)

    def test_recipe_get(self):
        c = Client()
        response = c.get(f"/recipe?id={self.recipe1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'], self.recipe1.id)
        self.assertEqual(response.context['name'], self.recipe1.name)
        self.assertEqual(float(response.context['volume_l']), self.recipe1.volume_l)
        self.assertEqual(response.context['descr'], self.recipe1.description)

    def test_recipe_post_anonymous(self):
        data = {'id': self.recipe1.id}
        c = Client()
        response = c.post(f"/recipe", data)
        self.assertEqual(response.status_code, 401)

    def test_recipe_post_bad_recipe_id(self):
        data = {'id': 100}
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.post("/recipe", data)
        self.assertEqual(response.status_code, 404)

    def test_recipe_post(self):
        data = {
            'id': self.recipe1.id,
            'name': 'recipe1x',
            'volume': 5.5,
            'descr': 'great new wine',
            'ingredient_id[]': [ 1 ],
            'ingredient_order[]': [ 0 ],
            'qty[]': [ 1.0 ],
        }
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.post(f"/recipe", data)
        self.assertEqual(response.status_code, 200)

    def test_newbrew_get_anonymous(self):
        c = Client()
        response = c.get(f"/newbrew?recipe_id={self.recipe1.id}")
        self.assertEqual(response.status_code, 401)

    def test_newbrew_get_bad_recipe_id(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get("/newbrew?recipe_id=100")
        self.assertEqual(response.status_code, 404)

    def test_newbrew_get(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get(f"/newbrew?recipe_id={self.recipe1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe_id'], self.recipe1.id)
        self.assertEqual(response.context['recipe']['name'], self.recipe1.name)

    def test_newbrew_post_anonymous(self):
        c = Client()
        response = c.post("/newbrew", None)
        self.assertEqual(response.status_code, 401)

    def test_newbrew_post_bad_recipe_id(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        data = {'recipe_id': 100}
        response = c.post("/newbrew", data)
        self.assertEqual(response.status_code, 404)

    def test_newbrew_post(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        num_brews = Brew.objects.all().count()
        data = {
            'recipe_id': self.recipe1.id,
            'volume': 5.0,
        }
        response = c.post("/newbrew", data)
        self.assertRedirects(response, f'/brew?id={Brew.objects.all().count()}')

    def test_brew_post(self):
        c = Client()
        response = c.post("/brew", None)
        self.assertEqual(response.status_code, 400)

    def test_brew_get_bad_id(self):
        c = Client()
        response = c.get("/brew?id=100")
        self.assertEqual(response.status_code, 404)

    def test_brew_get(self):
        c = Client()
        response = c.get(f"/brew?id={self.brew1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.context['brew']['id']), self.brew1.id)
        self.assertEqual(response.context['recipe']['name'], self.recipe1.name)
        self.assertEqual(response.context['tab'], '')
        self.assertEqual(bool(response.context['canModify']), False)

    def test_register_get(self):
        c = Client()
        response = c.get(f"/accounts/register")
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        c = Client()
        form = {
            'username': 'tony',
            'password1': 'tyxxyw4231G',
            'password2': 'tyxxyw4231G',
        }
        response = c.post(f"/accounts/register", form)
        self.assertRedirects(response, '/accounts/profile')

    def test_profile_get_anonymous(self):
        c = Client()
        response = c.get(f"/accounts/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_get(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get(f"/accounts/profile")
        self.assertEqual(response.status_code, 200)

    def test_profile_post_anonymous(self):
        c = Client()
        response = c.post(f"/accounts/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_post(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        profile = {
            'first_name': 'Tony',
            'last_name': 'Whittam',
            'location': 'Dublin',
            'solid_small_units': 0,
            'solid_large_units': 0,
            'liquid_small_units': 0,
            'liquid_large_units': 0,
        }
        response = c.post(f"/accounts/profile", profile)
        self.assertEqual(response.status_code, 200)
