from apps import organizers
from django.urls import path
from organizers import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("welcome", views.welcome, name="welcome"),
    # path("profiles/<organizer_id:str>", views.OrganizersView)
]
