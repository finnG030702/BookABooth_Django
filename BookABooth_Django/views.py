from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView
from .forms import CompanyForm, CustomPasswordResetForm, CustomUserCreationForm, CustomUserLoginForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm, LocationForm, BoothForm, ServicePackageForm
from .models import Company, System, Location, Booth, ServicePackage, Booking, TermsUpdateLog

User = get_user_model()


# Create your views here.

@login_required
@require_POST
def accept_privacy_policy(request):
    user = request.user
    user.privacy_policy_accepted = True
    user.save()
    return redirect("home")

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
    
class BookingListView(ListView):
    model = Booking
    template_name = "adminMenu/booking/booking_list.html"
    context_object_name = "bookings"

    def booking_table_partial(request):
        bookings = Booking.objects.all()
        return render(request, "adminMenu/booking/booking_table_body.html", {'bookings': bookings})
    
class BookingDetailView(DetailView):
    model = Booking
    template_name = "adminMenu/booking/booking_detail.html"

class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy("booking_list")

class CompanyDetailView(DetailView):
    model = Company
    template_name = "adminMenu/company/company_detail.html"

class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "adminMenu/company/company_form.html"

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk})
    
class WaitingListView(ListView):
    model = Company
    template_name = "adminMenu/waitingList/waitingList.html"
    context_object_name = "companies"

    def get_queryset(self):
        return Company.objects.order_by('-waiting_list', 'id')

    def waitinglist_table_partial(request):
        companies = Company.objects.order_by('-waiting_list', 'id')
        return render(request, "adminMenu/waitingList/waitinglist_table_body.html", {'companies': companies})
    
    def add_to_waitinglist(request, company_id):
        company = get_object_or_404(Company, id=company_id)
        company.waiting_list = True
        company.save()
        companies = Company.objects.order_by('-waiting_list', 'id')
        return render(request, "adminMenu/waitingList/waitinglist_table_body.html", {"companies": companies})
    
    def remove_from_waitinglist(request, company_id):
        company = get_object_or_404(Company, id=company_id)
        company.waiting_list = False
        company.save()
        companies = Company.objects.order_by('-waiting_list', 'id')
        return render(request, "adminMenu/waitingList/waitinglist_table_body.html", {"companies": companies})

class TermsResetView(LoginRequiredMixin, UserPassesTestMixin, View): # TODO: Alle Views nur für Admin machen
    template_name = "adminMenu/privacyPolicy/privacyPolicy.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        update_logs = TermsUpdateLog.objects.order_by('-updated_at')
        return render(request, self.template_name, {"logs": update_logs})

    def post(self, request):
        User.objects.update(privacy_policy_accepted=False)
        TermsUpdateLog.objects.create()
        return redirect("privacyPolicy")
