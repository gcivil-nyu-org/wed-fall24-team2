from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from .views import CustomLogoutView

app_name = "soundscape"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("get_user_sound_data/", views.get_user_sound_data, name="get_user_sound_data"),
    path("get_noise_data/", views.get_noise_data, name="get_noise_data"),
    path("check_profanity/", views.check_profanity, name="check_profanity"),
    path("filter_profanity/", views.filter_profanity, name="filter_profanity"),
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
    path("logout/", CustomLogoutView.as_view(), name="logout"),  # Fixed logout path
    path("validate_session/", views.validate_session, name="validate_session"),
]
