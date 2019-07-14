from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from core.views import PaginatedListView
from .models import Tag, Ingredient
from .forms.tag_forms import TagModelForm
from .forms.ingredient_forms import IngredientModelForm

##############
# Tag Mixins #
##############


class TagUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        if tag.user.id != self.request.user.id:
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
        if ingredient.user.id != self.request.user.id:
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
