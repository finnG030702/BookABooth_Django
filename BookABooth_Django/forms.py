from re import M
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms

from .models import Booth, Location, User, ServicePackage, Company

class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration.
    """
    company_name = forms.CharField(
        max_length=255,
        label="Firmenname"
    )

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            })

class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing user data. Will be used for the profile later.
    """

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)

class CustomUserLoginForm(AuthenticationForm):
    """
    Form for the login of users.
    """
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, request = ..., *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            })

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form for the user to change the password.
    """
    def __init__(self, user, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            })

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            })

class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetConfirmForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            })

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location', 'site_plan']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'site_plan': forms.ClearableFileInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
        }

class BoothForm(forms.ModelForm):
    """
    Form for the Booth-Admin Page. Styling for the fields, custom names for the labels. 
    """
    class Meta:
        model = Booth
        fields = ['title', 'ceiling_height', 'available', 'location', 'service_package']
        labels = {
            'title': "Bezeichnung",
            'ceiling_height': "Deckenhöhe (in m)",
            'available': "Verfügbar",
            'location': "Standort",
            'service_package': "Service-Pakete"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'ceiling_height': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-400 border-gray-300 rounded relative top-1.5'}),
            'location': forms.Select(attrs={
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
            'service_package': forms.SelectMultiple(attrs={
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
            })
        }

class ServicePackageForm(forms.ModelForm):
    class Meta:
        model = ServicePackage
        fields = ['name', 'price', 'description']
        labels = {
            'name': "Name",
            'price': "Preis in EUR",
            'description': "Beschreibung",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            }),
            'description': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
        }

class CompanyForm(forms.ModelForm):
    mail = forms.EmailField(
        required=True,
        label="E-Mail",
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

    class Meta:
        model = Company
        fields = ['name', 'billing_address', 'logo', 'description', 'waiting_list', 'exhibitor_list']
        labels = {
            'name': "Name",
            'billing_address': "Rechnungsadresse",
            'logo': "Logo",
            'description': "Firmenbeschreibung",
            'waiting_list': "Auf Warteliste",
            'exhibitor_list': "Auf Ausstellerliste",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'billing_address': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'description': forms.TextInput(attrs={'class': 'w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'waiting_list': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-400 border-gray-300 rounded relative top-1.5'}),
            'exhibitor_list': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-400 border-gray-300 rounded relative top-1.5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            user_qs = self.instance.employees.all()
            if user_qs.exists():
                first_user = user_qs.first()
                self.fields['mail'].initial = first_user.email
        

    def save(self, commit=True):
        company = super().save(commit)
        user_qs = company.employees.all()
        if user_qs.exists():
            first_user = user_qs.first()
            first_user.email = self.cleaned_data.get('mail')
            if commit:
                first_user.save()
        return company