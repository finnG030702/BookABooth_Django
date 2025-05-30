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
                    BoothListView, BoothCreateView, BoothDetailView, BoothUpdateView, BoothDeleteView,
                    ServicepackageListView, ServicepackageCreateView, ServicepackageDetailView, ServicepackageUpdateView, ServicepackageDeleteView,
                    BookingListView, BookingDetailView, BookingDeleteView,
                    CompanyDetailView, CompanyUpdateView, 
                    WaitingListView,
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

    path("booth/", BoothListView.as_view(), name="booth_list"),
    path("api/booth_list/", BoothListView.booth_table_partial, name="booth_table_partial"),
    path("booth/create/", BoothCreateView.as_view(), name="booth_create"),
    path("booth/<int:pk>/", BoothDetailView.as_view(), name="booth_detail"),
    path("booth/<int:pk>/edit/", BoothUpdateView.as_view(), name="booth_edit"),
    path("booth/<int:pk>/delete/", BoothDeleteView.as_view(), name="booth_delete"),

    path("service-package/", ServicepackageListView.as_view(), name="servicepackage_list"),
    path("api/service-package_list", ServicepackageListView.servicepackage_table_partial, name="servicepackage_table_partial"),
    path("service-package/create/", ServicepackageCreateView.as_view(), name="servicepackage_create"),
    path("service-package/<int:pk>/", ServicepackageDetailView.as_view(), name="servicepackage_detail"),
    path("service-package/<int:pk>/edit/", ServicepackageUpdateView.as_view(), name="servicepackage_edit"),
    path("service-package/<int:pk>/delete/", ServicepackageDeleteView.as_view(), name="servicepackage_delete"),

    path("booking/", BookingListView.as_view(), name="booking_list"),
    path("api/booking_list/", BookingListView.booking_table_partial, name="booking_table_partial"),
    path("booking/<int:pk>/", BookingDetailView.as_view(), name="booking_detail"),
    path("booking/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking_delete"),

    path("company/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path("company/<int:pk>/edit/", CompanyUpdateView.as_view(), name="company_edit"),

    path("waitinglist/", WaitingListView.as_view(), name="waitingList"),
    path("api/waitinglist/", WaitingListView.waitinglist_table_partial, name="waitinglist_partial"),
    path("waitinglist/add/<int:company_id>", WaitingListView.add_to_waitinglist, name="add_to_waitinglist"),
    path("waitinglist/remove/<int:company_id>", WaitingListView.remove_from_waitinglist, name="remove_from_waitinglist"),
]