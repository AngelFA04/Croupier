from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from raffles.forms import RaffleCreateForm


class RaffleCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    form_class = RaffleCreateForm
    template_name = "raffles/create_raffle.html"
    success_url = "/organizers/welcome"

    def get_initial(self):
        """Add the organizer to the form initial data."""
        self.initial["organizer"] = self.request.user.organizer
        return self.initial


class RaffleListView(LoginRequiredMixin, TemplateView):
    template_name = "raffles/list_raffles.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["raffles"] = request.user.organizer.raffles.all()
        return self.render_to_response(context)


class RaffleDetailView(LoginRequiredMixin, TemplateView):
    template_name = "raffles/detail_raffle.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RaffleProfile(LoginRequiredMixin, TemplateView):
    template_name = "raffles/profile.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["raffles"] = request.user.organizer.raffles.all()
        '''for _ in context["general"]:
            print(_)'''
        return self.render_to_response(context)


class RaffleFinishView(TemplateView):
    """
    View used to finish a raffle. And send the results to the raffle owner.
    """

    template_name = "raffles/finish_raffle.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
