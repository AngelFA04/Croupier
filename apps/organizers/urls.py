from django.urls import path
from organizers import views

from apps import organizers


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("welcome/", views.welcome, name="welcome"),
    path("me/", views.OrganizerProfileView.as_view(), name="profile"),
    path(
        "<str:pk>/", views.OrganizerPublicProfileView.as_view(), name="public_profile"
    ),
]
