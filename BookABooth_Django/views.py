from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView
from .forms import CustomPasswordResetForm, CustomUserCreationForm, CustomUserLoginForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm
from .models import Company, System

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

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
    """
    View for the Login of a user. If logged in, reverts back to home.html
    """
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"

class CustomPasswordChangeView(PasswordChangeView):
    """
    View for the Password Change. If changed, directs to password-change/done.
    """
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'

class PasswortResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    form_class = CustomPasswordResetForm

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    form_class = CustomPasswordResetConfirmForm

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

class SystemToggleView(View):
    template_name = "adminMenu/system_toggle.html"

    def get(self, request):
        system = System.objects.first()
        return render(request, self.template_name, {"system": system})
    
    def post(self, request):
        system = System.objects.first()
        enabled = request.POST.get("enabled") == "on"
        system.enabled = enabled
        system.save()
        return render(request, "adminMenu/_system_status.html", {"system": system})