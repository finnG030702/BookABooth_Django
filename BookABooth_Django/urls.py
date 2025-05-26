from django.urls import path

from .views import (HomeView,
                    CustomPasswordChangeView, 
                    SignUpView, 
                    LoginView, 
                    PasswortResetView, 
                    PasswordResetDoneView, 
                    PasswordResetConfirmView, 
                    PasswordResetCompleteView, 
                    SystemToggleView, 
                    )

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_reset/", PasswortResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("system/", SystemToggleView.as_view(), name="system"),
    path("system/toggle/", SystemToggleView.as_view(), name="system_toggle"),
]