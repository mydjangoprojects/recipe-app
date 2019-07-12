from django import forms

from recipe.models import Tag


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', ]
