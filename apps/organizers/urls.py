from django.urls import path
from organizers import views

from apps import organizers


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("welcome", views.welcome, name="welcome"),
    # path("profiles/<organizer_id:str>", views.OrganizersView)
]
