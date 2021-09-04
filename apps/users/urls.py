from django.urls import path
from users import views

urlpatterns = [
    # TODO Move signup to users
    # path("signup", "users.views.login", name="login"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
]
