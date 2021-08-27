from apps import organizers
from django.urls import path
from raffles.views import RaffleView


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    # TODO Add the views for the raffles
    path("create", RaffleView.as_view(), name="create-raffle"),
    path("list", RaffleView.as_view(), name="list-raffle"),
    path("find/", RaffleView.as_view(), name="find-raffle"),
    path("detail/<str:raffle_id>", RaffleView.as_view(), name="create-list"),
    path("detail/<str:raffle_id>", RaffleView.as_view(), name="create-list"),
]
