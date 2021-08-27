from apps import organizers
from django.urls import path
from raffles import views


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    # TODO Add the views for the raffles
    path("create", views.RaffleCreateView.as_view(), name="create-raffle"),
    path("list", views.RaffleListView.as_view(), name="list-raffle"),
    path("finish", views.RaffleFinishView.as_view(), name="finish-raffle"),
    # path("find/", views.RaffleView.as_view(), name="find-raffle"),
    path("detail/<str:raffle_id>", views.RaffleDetailView.as_view(), name="detail-raffle"),
]
