from rest_framework import viewsets, serializers
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404

class RequestViewSet(viewsets.ModelViewSet):
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    model = Recipe
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title',]
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def perform_update(self, serializer):
        # /recipe/recipe/<pk>/
        pk = self.kwargs['pk']
        author_id = get_object_or_404(Recipe, pk=pk).author.id
        if author_id == self.request.user.id:
            serializer.save(author=self.request.user)
        else:
            raise serializers.ValidationError('このレシピを更新できません')

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError('このレシピは削除できません')
            
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    model = Ingredient

    def perform_create(self, serializer):
        recipe = serializer.validated_data['recipe']
        if recipe.author == self.request.user:
            serializer.save(recipe=recipe)
        else:
            raise serializers.ValidationError('このレシピに材料を追加できません')
        
    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        ingredient = get_object_or_404(Ingredient, pk=pk)
        recipe = ingredient.recipe
        if recipe.author == self.request.user:
            serializer.save(recipe=recipe)
        else:
            raise serializers.ValidationError('このレシピに材料を追加できません')
        
    def perform_destroy(self, instance):
        if instance.recipe.author == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError('この材料は削除できません')