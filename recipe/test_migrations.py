from django.test import TestCase
from django_test_migrations.contrib.unittest_case import MigratorTestCase

class ReverseIngredientsMigrationTestCase(MigratorTestCase):
    migrate_from = ('recipe', '0004_auto_20200616_2008')
    migrate_to = ('recipe', '0003_method_method_num')

    def prepare(self):
        pass

    def test_migration(self):
        Ingredient = self.new_state.apps.get_model('recipe', 'Ingredient')
        Method = self.new_state.apps.get_model('recipe', 'Method')

        self.assertEqual(Ingredient.objects.count(), 0)
        self.assertEqual(Method.objects.count(), 0)

class ReverseWinestyleMigrationTestCase(MigratorTestCase):
    migrate_from = ('recipe', '0006_auto_20200617_1402')
    migrate_to = ('recipe', '0005_auto_20200617_1357')

    def prepare(self):
        pass

    def test_migration(self):
        WineStyle = self.new_state.apps.get_model('recipe', 'WineStyle')

        self.assertEqual(WineStyle.objects.count(), 0)

class ReverseIngredientsUpdateMigrationTestCase(MigratorTestCase):
    migrate_from = ('recipe', '0018_auto_20200813_1504')
    migrate_to = ('recipe', '0017_ingredient_is_solid')

    def prepare(self):
        pass

    def test_migration(self):
        Ingredient = self.new_state.apps.get_model('recipe', 'Ingredient')
        old_default_qty = 0.2

        for ingredient in Ingredient.objects.all():
            self.assertEqual(ingredient.default_qty_kg_per_l, old_default_qty)
        
        self.assertEqual(Ingredient.objects.get(name='Elderflowers').liquid, 1000.0)
        self.assertEqual(Ingredient.objects.get(name='Sugar').liquid, 500.0)
        self.assertEqual(Ingredient.objects.get(name='Sugar for sweetening').liquid, 500.0)
