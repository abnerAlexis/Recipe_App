from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.CharField(max_length=500, help_text="Separate each ingredient with a comma", blank=False, null=False)
    cooking_time = models.IntegerField(blank=False, null=False)
    difficulty = models.CharField(max_length=20, editable=False)
    instructions = models.TextField()
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')


    def calculate_difficulty(self):
        ingredient_count = len([i.strip() for i in self.ingredients.split(",")])
        if self.cooking_time < 10 and ingredient_count < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and ingredient_count >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and ingredient_count < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    
    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation occurs before saving
        self.calculate_difficulty()
        super().save(*args, **kwargs)


    def clean(self):
        # Validate cooking time
        if not self.cooking_time > 0:
            raise ValidationError('Cooking time must be greater than zero.')
        
        # Validate ingredients
        if not self.ingredients.strip():
            raise ValidationError('Ingredients cannot be blank.')
        

    def get_absolute_url(self):
        return reverse ("recipes:detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return (
            f"{self.name}, Ingredients: {self.ingredients}, "
            f"Cooking Time: {self.cooking_time} minutes, "
            f"Difficulty: {self.difficulty}, Instructions: {self.instructions}"
        )