import os
import uuid

from django.conf import settings
from django.db import models


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    if str(filename).find('.') == -1:
        raise ValueError(
            'The filename must contain a "." symbol and extension.'
            )

    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class Tag(models.Model):
    """Tag to be used for a recipe"""

    class Meta:
        ordering = ['-id']

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(verbose_name="Creation Date",
                                      auto_now_add=True)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super(Tag, self).save_model(request, obj, form, change)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""

    class Meta:
        ordering = ['-id']

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(verbose_name="Creation Date",
                                      auto_now_add=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""

    class Meta:
        ordering = ['-id']

    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time_minutes = models.IntegerField()
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    created_on = models.DateTimeField(verbose_name="Creation Date",
                                      auto_now_add=True)

    def __str__(self):
        return self.title
