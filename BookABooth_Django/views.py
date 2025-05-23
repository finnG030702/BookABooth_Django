from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomPasswordChangeForm
from .models import Company

# Create your views here.

class SignUpView(CreateView):
    """
    View for registration of a new user. The company comes from a different model.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        company_name = form.cleaned_data["company_name"]
        company, _ = Company.objects.get_or_create(name=company_name) # Gibt Company und ein Boolean zurück. _ weil created (bool) egal ist.

        user = form.save(commit=False)
        user.company = company
        user.save()

        return super().form_valid(form)

class LoginView(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'