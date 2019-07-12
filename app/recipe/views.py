from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from core.views import PaginatedListView
from .models import Tag
from .forms.tag_forms import TagModelForm


#############
# Tag Views #
#############


class TagList(LoginRequiredMixin, PaginatedListView):
    model = Tag
    template_name = 'tag/tag_list.html'
    paginate_by = 5
    queryset = Tag.objects.all()


class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'tag/tag_detail.html'


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = 'tag/tag_update.html'
    fields = ['name', ]
    success_url = reverse_lazy('recipe:tag_list')


class TagDelete(LoginRequiredMixin, DeleteView):
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
