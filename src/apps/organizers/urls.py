from django.urls import path
from organizers import views


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signup/", views.get_name, name="signup"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("welcome", views.welcome, name="welcome"),
]
