from django import views
from django.http.request import HttpRequest
from django.shortcuts import render


class HomeView(views.View):
    """
    View for the app home page.
    """

    def get(self, request: HttpRequest):
        """
        Handles GET requests.
        """
        context = {
            "title": "Croupier",
        }
        return render(request, "home.html", context)
