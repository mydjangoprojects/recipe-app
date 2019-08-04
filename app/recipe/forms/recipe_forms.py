from django.forms import (
    ModelMultipleChoiceField,
    CharField, FloatField,
    ImageField, IntegerField,

    TextInput, FileInput,
    NumberInput, ModelForm,
)

from recipe.models import Recipe, Tag, Ingredient, recipe_image_file_path


class RecipeModelForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class': 'input-field col s6'}))
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all())
    ingredients = ModelMultipleChoiceField(queryset=Ingredient.objects.all())
    price = FloatField(widget=NumberInput())
    time_minutes = IntegerField(widget=NumberInput())
    image = ImageField()

    class Meta:
        model = Recipe
        fields = ['title',
                  'price',
                  'tags',
                  'ingredients',
                  'time_minutes',
                  'image']
