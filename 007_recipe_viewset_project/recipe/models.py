from django.db import models
from user.models import CustomUser

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    instruction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        CustomUser, related_name='recipes',
        on_delete=models.CASCADE
    )

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe,
                               related_name='ingredients',
                               on_delete=models.CASCADE)
    
