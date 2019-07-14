from django import forms

from recipe.models import Ingredient


class IngredientModelForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', ]
