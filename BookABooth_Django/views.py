from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView
from .forms import CustomPasswordResetForm, CustomUserCreationForm, CustomUserLoginForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm, LocationForm, BoothForm, ServicePackageForm
from .models import Company, System, Location, Booth, ServicePackage

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
    """
    View for the SystemToggle.html. Changes the enabled-Attribute of system in its response.
    """
    template_name = "adminMenu/system/system_toggle.html"

    def get(self, request):
        system = System.objects.first()
        return render(request, self.template_name, {"system": system})
    
    def post(self, request):
        system = System.objects.first()
        enabled = request.POST.get("enabled") == "on"
        system.enabled = enabled
        system.save()
        return render(request, "adminMenu/system/_system_status.html", {"system": system})
    
class LocationListView(ListView):
    model = Location
    template_name = "adminMenu/location/location_list.html"
    context_object_name = 'locations'

    def location_table_partial(request):
        locations = Location.objects.all()
        return render(request, "adminMenu/location/location_table_body.html", {"locations": locations})

class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = "adminMenu/location/location_form.html"
    success_url = reverse_lazy("location_list")

class LocationDetailView(DetailView):
    model = Location
    template_name = "adminMenu/location/location_detail.html"

class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "adminMenu/location/location_form.html"
    success_url = reverse_lazy("location_list")

class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy("location_list")

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class BoothListView(ListView):
    model = Booth
    template_name = "adminMenu/booth/booth_list.html"
    context_object_name = 'booths'

    def booth_table_partial(request):
        booths = Booth.objects.all()
        return render(request, "adminMenu/booth/booth_table_body.html", {"booths": booths})
    
class BoothCreateView(CreateView):
    model = Booth
    form_class = BoothForm
    template_name = "adminMenu/booth/booth_form.html"
    success_url = reverse_lazy("booth_list")

class BoothDetailView(DetailView):
    model = Booth
    template_name = "adminMenu/booth/booth_detail.html"

class BoothUpdateView(UpdateView):
    model = Booth
    form_class = BoothForm
    template_name = "adminMenu/booth/booth_form.html"
    success_url = reverse_lazy("booth_list")

class BoothDeleteView(DeleteView):
    model = Booth
    success_url = reverse_lazy("booth_list")

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class ServicepackageListView(ListView):
    model = ServicePackage
    template_name = "adminMenu/servicepackage/servicepackage_list.html"
    context_object_name = 'servicepackages'

    def servicepackage_table_partial(request):
        servicepackages = ServicePackage.objects.all()
        return render(request, "adminMenu/servicepackage/servicepackage_table_body.html", {"servicepackages": servicepackages})
    
class ServicepackageCreateView(CreateView):
    model = ServicePackage
    form_class = ServicePackageForm
    template_name = "adminMenu/servicepackage/servicepackage_form.html"
    success_url = reverse_lazy("servicepackage_list")

class ServicepackageDetailView(DetailView):
    model = ServicePackage
    template_name = "adminMenu/servicepackage/servicepackage_detail.html"

class ServicepackageUpdateView(UpdateView):
    model = ServicePackage
    form_class = ServicePackageForm
    template_name = "adminMenu/servicepackage/servicepackage_form.html"
    success_url = reverse_lazy("servicepackage_list")

class ServicepackageDeleteView(DeleteView):
    model = ServicePackage
    success_url = reverse_lazy("servicepackage_list")

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)