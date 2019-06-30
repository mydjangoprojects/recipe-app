from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUp(generic.edit.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    class Meta:
        model = User
