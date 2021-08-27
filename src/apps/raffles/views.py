from django.shortcuts import render
from django.views.generic import TemplateView


class RaffleView(TemplateView):
    template_name = "raffles/raffle.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        pass
