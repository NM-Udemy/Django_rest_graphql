from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RecipeViewSet, IngredientViewSet

router = DefaultRouter()
router.register('recipe', RecipeViewSet, basename='recipe')
router.register('ingredient', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls))
]