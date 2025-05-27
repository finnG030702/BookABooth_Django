from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms

from .models import Location, User

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