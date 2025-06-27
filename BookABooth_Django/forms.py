from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import Booth, Location, User, ServicePackage, Company

INPUT_STYLE = "w-full bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
CHECKBOX_STYLE = "h-5 w-5 text-blue-600 focus:ring-blue-400 border-gray-300 rounded relative top-1.5"


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration.
    """
    company_name = forms.CharField(
        max_length=255,
        label="Firmenname"
    )
    privacy_policy_accepted = forms.BooleanField(
        label=mark_safe(
            'Ich habe die <a href="https://www.jade-hs.de/datenschutz" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">Datenschutzerklärung</a> gelesen und akzeptiert'),
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-400 border-gray-300 rounded'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })

    def clean_company_name(self):
        """
        Checks that the company doesn't already exist. Raises Error if it does.
        """
        name = self.cleaned_data['company_name']
        if Company.objects.filter(name__iexact=name).exists():
            raise ValidationError("Der Firmenname ist bereits vergeben.")
        return name


class CustomUserChangeForm(forms.ModelForm):
    """
    Form for changing user data. Will be used for the profile later.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        labels = {
            "first_name": "Vorname Ansprechpartner",
            "last_name": "Nachname Ansprechpartner",
            "phone": "Telefonnummer Ansprechpartner",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={
                'placeholder': "Ihr Vorname",
            }),
            "last_name": forms.TextInput(attrs={
                'placeholder': "Ihr Nachname",
            }),
            "email": forms.EmailInput(attrs={
                'placeholder': "Ihre E-Mail-Adresse",
            }),
            "phone": forms.TextInput(attrs={
                'placeholder': "Ihre Telefonnummer",
            })
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })


class CustomCompanyChangeForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "billing_address", "comment", "description", "logo", "exhibitor_list")
        labels = {
            "name": "Firmenname",
            "billing_address": "Rechnungsanschrift",
            "comment": "Bemerkung, wird für Rechnung übernommen",
            "description": "Kurze Beschreibung Ihres Unternehmens (max. 1024 Zeichen)",
            "logo": "Unternehmenslogo",
            "exhibitor_list": "Freigabe Ausstellerliste",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                'class': INPUT_STYLE,
                'placeholder': "Name Ihres Unternehmens"
            }),
            "billing_address": forms.Textarea(attrs={
                'class': INPUT_STYLE,
                'rows': 2,
                'placeholder': "Straße Hausnummer // PLZ Ort"
            }),
            "comment": forms.Textarea(attrs={
                'class': INPUT_STYLE,
                'rows': 1,
                'placeholder': "Bemerkung"
            }),
            "description": forms.Textarea(attrs={
                'class': INPUT_STYLE,
                'rows': 3,
                'placeholder': "Beschreibung Ihres Unternehmens"
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': INPUT_STYLE
            }),
            'exhibitor_list': forms.CheckboxInput(attrs={
                'class': CHECKBOX_STYLE
            }),
        }


class CustomUserLoginForm(AuthenticationForm):
    """
    Form for the login of users.
    """

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, request=..., *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form for the user to change the password.
    """

    def __init__(self, user, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })


class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetConfirmForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE,
            })


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location', 'site_plan']
        widgets = {
            'location': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'site_plan': forms.ClearableFileInput(attrs={'class': INPUT_STYLE}),
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
            'title': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'ceiling_height': forms.NumberInput(attrs={
                'step': '0.01',
                'class': INPUT_STYLE}),
            'available': forms.CheckboxInput(attrs={'class': CHECKBOX_STYLE}),
            'location': forms.Select(attrs={
                'class': INPUT_STYLE
            }),
            'service_package': forms.SelectMultiple(attrs={
                'class': INPUT_STYLE
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
            'name': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'class': INPUT_STYLE,
            }),
            'description': forms.TextInput(attrs={'class': INPUT_STYLE}),
        }


class CompanyForm(forms.ModelForm):
    mail = forms.EmailField(
        required=True,
        label="E-Mail",
        widget=forms.EmailInput(attrs={
            'class': INPUT_STYLE
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
            'name': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'billing_address': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'logo': forms.ClearableFileInput(attrs={'class': INPUT_STYLE}),
            'description': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'waiting_list': forms.CheckboxInput(attrs={'class': CHECKBOX_STYLE}),
            'exhibitor_list': forms.CheckboxInput(attrs={'class': CHECKBOX_STYLE}),
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
