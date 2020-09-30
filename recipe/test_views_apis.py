from django.test import TestCase, Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

from .models import Ingredient, Method, Recipe, IngredientUse, Brew, LogEntry, Comment, Image, WineStyle, Profile

class ApiTestCase(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="user1_pw")
        profile1 = Profile.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username="user2", password="user2_pw")
        profile2 = Profile.objects.create(user=self.user2)
        admin = User.objects.create_user(username="admin", password="admin_pw")
        admin.is_superuser = True
        admin.save()

        # Get styles
        styles = WineStyle.objects.all()

        # Get ingredients
        ingredients = Ingredient.objects.all()

        # Some dates to use in the records
        today = date.today()
        today_minus_1 = date.today() - timedelta(days=1)
        today_minus_2 = date.today() - timedelta(days=2)
        today_minus_3 = date.today() - timedelta(days=3)
        today_minus_4 = date.today() - timedelta(days=4)
        today_minus_5 = date.today() - timedelta(days=5)
        today_minus_6 = date.today() - timedelta(days=6)
        today_minus_7 = date.today() - timedelta(days=7)
        today_minus_8 = date.today() - timedelta(days=8)
        today_minus_9 = date.today() - timedelta(days=9)
        today_minus_10 = date.today() - timedelta(days=10)
        today_minus_11 = date.today() - timedelta(days=11)
        today_minus_12 = date.today() - timedelta(days=12)
        today_minus_13 = date.today() - timedelta(days=13)
        today_minus_14 = date.today() - timedelta(days=14)

        # Create recipes
        self.recipe1 = Recipe.objects.create(name='recipe1', style=styles[0], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_14)
        self.recipe2 = Recipe.objects.create(name='recipe2', style=styles[1], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_13)
        Recipe.objects.create(name='recipe3', style=styles[2], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_12)
        Recipe.objects.create(name='recipe4', style=styles[3], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_11)
        Recipe.objects.create(name='recipe5', style=styles[0], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_10)
        Recipe.objects.create(name='recipe6', style=styles[1], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_9)
        Recipe.objects.create(name='recipe7', style=styles[2], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_8)
        Recipe.objects.create(name='recipe8', style=styles[3], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_7)
        Recipe.objects.create(name='recipe9', style=styles[0], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_6)
        Recipe.objects.create(name='recipe10', style=styles[1], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_5)
        Recipe.objects.create(name='recipe11', style=styles[2], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_4)
        Recipe.objects.create(name='recipe12', style=styles[3], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_3)
        Recipe.objects.create(name='recipe13', style=styles[0], volume_l=5.0, created_by=self.user1,
            create_date=today_minus_2)
        Recipe.objects.create(name='recipe14', style=styles[1], volume_l=5.0, created_by=self.user2,
            create_date=today_minus_1)

        # Add ingredients to recipes
        IngredientUse.objects.create(recipe=self.recipe1, ingredient=ingredients[0], qty_kg=1.0, order=0)
        IngredientUse.objects.create(recipe=self.recipe1, ingredient=ingredients[1], qty_kg=2.0, order=1)
        IngredientUse.objects.create(recipe=self.recipe2, ingredient=ingredients[2], qty_kg=0.5, order=0)

        # Create Brews
        brew1 = Brew.objects.create( user=self.user1, recipe=self.recipe1, size_l=5.0, started=today_minus_14, updated=today_minus_1)
        brew2 = Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_13, updated=today_minus_2)
        Brew.objects.create( user=self.user1, recipe=self.recipe1, size_l=5.0, started=today_minus_12, updated=today_minus_12)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_11, updated=today_minus_11)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_10, updated=today_minus_10)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_9, updated=today_minus_9)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_8, updated=today_minus_8)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_7, updated=today_minus_7)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_6, updated=today_minus_6)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_5, updated=today_minus_5)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_4, updated=today_minus_4)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_3, updated=today_minus_3)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_2, updated=today_minus_2)
        Brew.objects.create( user=self.user2, recipe=self.recipe2, size_l=5.0, started=today_minus_1, updated=today_minus_1)

        # Create brew log entries
        logentry1 = LogEntry.objects.create(user=self.user1, brew=brew1, text='entry1', datetime=datetime.now()-timedelta(days=2))
        logentry2 = LogEntry.objects.create(user=self.user1, brew=brew1, text='entry2', datetime=datetime.now()-timedelta(days=1))
        LogEntry.objects.create(user=self.user2, brew=brew2, text='entry3', datetime=datetime.now()-timedelta(days=2))

        # Create log entry comments
        Comment.objects.create(user=self.user1, brew=brew1, text='comment1',logEntry=logentry1,datetime=datetime.now()-timedelta(days=2))
        Comment.objects.create(user=self.user2, brew=brew1, text='comment2',logEntry=logentry1,datetime=datetime.now()-timedelta(days=1))

    def test_recipelist_single_ordered(self):
        c = Client()
        response = c.get("/api/recipelist?order=name")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recipes']),14)
        self.assertEqual(response.json()['recipes'][0]['name'], 'recipe1')
        self.assertEqual(response.json()['recipes'][13]['name'], 'recipe9')
        lastRecipe = None
        for recipe in response.json()['recipes']:
            if lastRecipe != None:
                self.assertGreaterEqual(recipe['name'], lastRecipe['name'])
            lastRecipe = recipe

    def test_recipelist_indirect_double_ordered(self):
        c = Client()
        response = c.get("/api/recipelist?order=style__grapes,style__region")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recipes']),14)
        lastRecipe = None
        for recipe in response.json()['recipes']:
            if lastRecipe != None:
                self.assertGreaterEqual(recipe['style']['grapes'], lastRecipe['style']['grapes'])
                if recipe['style']['grapes'] == lastRecipe['style']['grapes']:
                    self.assertGreaterEqual(recipe['style']['region'], lastRecipe['style']['region'])
            lastRecipe = recipe

    def test_recipelist_only_current_user(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get("/api/recipelist?order=name&thisUserOnly=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recipes']),7)
        for recipe in response.json()['recipes']:
            self.assertEqual(recipe['created_by'], 'user1')

    def test_recipelist_recent(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get("/api/recipelist?recent=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recipes']),10)

    def test_recipe_invalid_id_anonymous(self):
        c = Client()
        response = c.get("/api/recipe?id=-1")
        self.assertEqual(response.json()['recipe']['id'], -1)
        self.assertEqual(response.json()['profile'], None)

    def test_recipe(self):
        c = Client()
        c.login(username='user1', password='user1_pw')
        response = c.get(f"/api/recipe?id={self.recipe1.id}")
        self.assertEqual(response.json()['recipe']['name'], self.recipe1.name)
        self.assertEqual(response.json()['profile']['user_id'], self.user1.id)
