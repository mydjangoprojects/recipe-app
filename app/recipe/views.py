from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from core.views import PaginatedListView
from .models import Tag, Ingredient, Recipe
from .forms.tag_forms import TagModelForm
from .forms.ingredient_forms import IngredientModelForm
from .forms.recipe_forms import RecipeModelForm

##############
# Tag Mixins #
##############


class TagUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        req_user = self.request.user

        if not req_user.is_staff and not req_user.is_superuser:
            if tag.user.id != req_user.id:
                return False

        return True


#############
# Tag Views #
#############

class TagList(LoginRequiredMixin, PaginatedListView):
    model = Tag
    template_name = 'tag/tag_list.html'
    queryset = Tag.objects.all()


class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'tag/tag_detail.html'


class TagUpdate(LoginRequiredMixin, TagUserPassesTestMixin, UpdateView):
    model = Tag
    form_class = TagModelForm
    template_name = 'tag/tag_update.html'


class TagDelete(LoginRequiredMixin, TagUserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'tag/tag_delete.html'
    success_url = reverse_lazy('recipe:tag_list')


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagModelForm
    template_name = 'tag/tag_create.html'
    success_url = reverse_lazy('recipe:tag_list')

    def form_valid(self, form):
        form.save(commit=False)
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(TagCreate, self).form_valid(form)


#####################
# Ingredient Mixins #
#####################

class IngredientUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        ingredient = Ingredient.objects.get(pk=self.kwargs['pk'])
        req_user = self.request.user

        if not req_user.is_staff and not req_user.is_superuser:
            if ingredient.user.id != req_user.id:
                return False

        return True


####################
# Ingredient Views #
####################

class IngredientList(LoginRequiredMixin, PaginatedListView):
    model = Ingredient
    template_name = 'ingredient/ingredient_list.html'
    queryset = Ingredient.objects.all()


class IngredientDetail(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = 'ingredient/ingredient_detail.html'


class IngredientUpdate(LoginRequiredMixin,
                       IngredientUserPassesTestMixin,
                       UpdateView):
    model = Ingredient
    form_class = IngredientModelForm
    template_name = 'ingredient/ingredient_update.html'


class IngredientDelete(LoginRequiredMixin,
                       IngredientUserPassesTestMixin,
                       DeleteView):
    model = Ingredient
    template_name = 'ingredient/ingredient_delete.html'
    success_url = reverse_lazy('recipe:ingredient_list')


class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientModelForm
    template_name = 'ingredient/ingredient_create.html'
    success_url = reverse_lazy('recipe:ingredient_list')

    def form_valid(self, form):
        form.save(commit=False)
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(IngredientCreate, self).form_valid(form)


#################
# Recipe Mixins #
#################

class RecipeUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        req_user = self.request.user

        if not req_user.is_staff or not req_user.is_superuser:
            if recipe.user.id != req_user.id:
                return False

        return True


################
# Recipe Views #
################

class RecipeList(LoginRequiredMixin, PaginatedListView):
    model = Recipe
    queryset = Recipe.objects.all()
    template_name = 'recipe/recipe_list.html'


class RecipeDetail(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'


class RecipeUpdate(LoginRequiredMixin, RecipeUserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'recipe/recipe_update.html'
    success_url = reverse_lazy('recipe:recipe_list')


class RecipeDelete(LoginRequiredMixin, RecipeUserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = reverse_lazy('recipe:recipe_list')


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'recipe/recipe_create.html'
    success_url = reverse_lazy('recipe:recipe_list')

    def form_valid(self, form):
        form.save(commit=False)
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(RecipeCreate, self).form_valid(form)
