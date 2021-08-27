from django.urls import path
from users import views

urlpatterns = [
    # TODO Move signup to users
    # path("signup", "users.views.login", name="login"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]
