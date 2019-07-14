from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm

User = get_user_model()


class SignUp(generic.edit.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    class Meta:
        model = User


class PaginatedListView(generic.ListView):
    """This class will contain the common base implementation for
       List Views with pagination"""

    # Default
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.queryset
        objects, page_range = self.initialize_paginator(queryset)

        # Context Update
        context = super(PaginatedListView, self).get_context_data(**kwargs)
        context.update({
            'list_objects': objects,
            'page_range': page_range,
        })

        return context

    def initialize_paginator(self, queryset):
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except TypeError:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        index = objects.number - 1

        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        return objects, page_range
