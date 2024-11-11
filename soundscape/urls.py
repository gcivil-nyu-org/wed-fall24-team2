from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from django.contrib.auth.views import LogoutView

app_name = "soundscape"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("get_noise_data/", views.get_noise_data, name="get_noise_data"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="soundscape/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/", LogoutView.as_view(next_page="/"), name="logout"
    ),  # Redirect to homepage after logout
]
