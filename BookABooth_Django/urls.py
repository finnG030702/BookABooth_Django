from django.urls import path

from .views import CustomPasswordChangeView, SignUpView, LoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change")
]