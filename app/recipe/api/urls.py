from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.api import view_sets

router = DefaultRouter()
router.register('tags', view_sets.TagViewSet)
router.register('ingredients', view_sets.IngredientViewSet)
router.register('recipes', view_sets.RecipeViewSet)

app_name = 'recipe.api'

urlpatterns = [
    path('', include(router.urls)),
]
