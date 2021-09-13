from django.urls import path
from raffles import views

from apps import organizers


urlpatterns = [
    path("", views.RaffleListPublicView.as_view(), name="public-list-raffles"),
    path(
        "public/<str:pk>",
        views.RaffleListPublicView.as_view(),
        name="public-list-raffles",
    ),
    # TODO Add the views for the raffles
    path("create", views.RaffleCreateView.as_view(), name="create-raffle"),
    path("list", views.RaffleListView.as_view(), name="list-raffle"),
    path("finish", views.RaffleFinishView.as_view(), name="finish-raffle"),
    # path("find/", views.RaffleView.as_view(), name="find-raffle"),
    path("detail/<str:pk>", views.RaffleDetailView.as_view(), name="detail-raffle"),
    path(
        "detail/<str:pk>/update", views.RaffleUpdateView.as_view(), name="update-raffle"
    ),
    path(
        "detail/<str:pk>/publicate",
        views.RafflePublicateView.as_view(),
        name="publicate-raffle",
    ),
    path("detail/<str:pk>/tickets", views.TicketListView.as_view(), name="list-ticket"),
]
