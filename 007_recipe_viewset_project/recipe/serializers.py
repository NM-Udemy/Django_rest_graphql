from .models import Recipe, Ingredient
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'quantity', 'recipe')
        read_only_fields = ('id', )
    
    # def validate(self, data):
    #     recipe = get_object_or_404(Recipe, pk=data['recipe'].id)
    #     user = self.context['request'].user
    #     if recipe.author != user:
    #         raise serializers.ValidationError('このレシピに材料を更新できません')
    #     return data
    

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'instruction', 'author', 'ingredients')
        read_only_fields = ('id', 'author')
    
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     return Recipe.objects.create(author=user, **validated_data)
