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
                    LocationListView, LocationCreateView, LocationDetailView, LocationUpdateView, LocationDeleteView, 
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
    path("location/", LocationListView.as_view(), name="location_list"),
    path("api/location_list", LocationListView.location_table_partial, name="location_table_partial"),
    path("location/create/", LocationCreateView.as_view(), name="location_create"),
    path("location/<int:pk>/", LocationDetailView.as_view(), name="location_detail"),
    path("location/<int:pk>/edit/", LocationUpdateView.as_view(), name="location_edit"),
    path("location/<int:pk>/delete/", LocationDeleteView.as_view(), name="location_delete"),
]