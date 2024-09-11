# Create your tests here.
from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a recipe instance for testing
        cls.recipe_instance = Recipe.objects.create(
            name='Oven Roasted Broccoli Cheese',
            ingredients='broccoli, cheddar, olive oil, salt, pepper',
            cooking_time=20,
            instructions='Toss broccoli with olive oil, salt, and pepper, then roast in the oven at 425°F (220°C) for 15-20 minutes, sprinkling cheddar cheese on top during the last 5 minutes of cooking.'
        )

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_recipe_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        recipe.calculate_difficulty()
        recipe.save()
        self.assertEqual(recipe.difficulty, "Hard")

    def test_ingredients_field(self):
        recipe = Recipe.objects.get(id=1)
        # Check if the ingredients are saved correctly
        self.assertEqual(recipe.ingredients, 'broccoli, cheddar, olive oil, salt, pepper')
        # Check the maximum length of ingredients
        max_length = recipe._meta.get_field('ingredients').max_length
        self.assertEqual(max_length, 500)

    def test_cooking_time_field(self):
        recipe = Recipe.objects.get(id=1)
        # Check if the cooking time is saved correctly
        self.assertEqual(recipe.cooking_time, 20)
        
        # Check if cooking time is greater than zero
        self.assertGreater(recipe.cooking_time, 0)

    def test_instructions_field(self):
        recipe = Recipe.objects.get(id=1)
        # Check if the instructions are saved correctly
        self.assertEqual(recipe.instructions, 'Toss broccoli with olive oil, salt, and pepper, then roast in the oven at 425°F (220°C) for 15-20 minutes, sprinkling cheddar cheese on top during the last 5 minutes of cooking.')

    def test_get_absolute_url(self):
       recipe = Recipe.objects.get(id=1)
       #get_absolute_url() should take you to the detail page of recipe #1
       #and load the URL /recipes/list/1
       self.assertEqual(recipe.get_absolute_url(), '/list/1/')


class RecipeModelMethodTest(TestCase):

    def test_calculate_difficulty_easy(self):
        recipe = Recipe.objects.create(
            name='Easy Recipe',
            ingredients='ingredient1, ingredient2',
            cooking_time=10,
            instructions='Some instructions.'
        )
        recipe.calculate_difficulty()
        recipe.save()
        self.assertEqual(recipe.difficulty, 'Intermediate')

    def test_calculate_difficulty_hard(self):
        recipe = Recipe.objects.create(
            name='Hard Recipe',
            ingredients='ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6',
            cooking_time=60,
            instructions='Some instructions.'
        )
        recipe.calculate_difficulty()
        recipe.save()
        self.assertEqual(recipe.difficulty, 'Hard')