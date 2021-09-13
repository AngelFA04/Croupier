from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from raffles.forms import RaffleCreateForm
from raffles.forms import RaffleDetailForm
from raffles.forms import RafflePublicateForm
from raffles.forms import RaffleUpdateForm
from raffles.forms import TicketListForm
from raffles.models import RaffleModel


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
        # breakpoint()
        return self.render_to_response(context)


class RaffleDetailView(LoginRequiredMixin, DetailView):
    template_name = "raffles/detail_raffle.html"
    model = RaffleModel

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = RaffleUpdateForm(request.POST, instance=self.object)
        context["form"] = form
        if form.is_valid():
            form.save()
            return self.render_to_response(context)
        else:
            context["form"] = form
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["form"] = RaffleDetailForm(instance=self.object)
        # breakpoint()
        return self.render_to_response(context)


class RaffleUpdateView(LoginRequiredMixin, DetailView):
    template_name = "raffles/update_raffle.html"
    model = RaffleModel

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["form"] = RaffleUpdateForm(instance=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = RaffleUpdateForm(request.POST, instance=self.object)
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("detail-raffle", pk=self.object.pk)
            # return self.render_to_response(context)
        else:
            context["form"] = form
            return self.render_to_response(context)


class RafflePublicateView(LoginRequiredMixin, DetailView):
    """
    View used to finish a raffle. And send the results to the raffle owner.
    """

    template_name = "raffles/public_raffle.html"
    form_class = RafflePublicateForm
    model_class = RaffleModel

    def get_queryset(self):
        return self.model_class.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        form.save()
        return redirect("detail-raffle", pk=self.object.pk)


class RaffleFinishView(TemplateView):
    """
    View used to finish a raffle. And send the results to the raffle owner.
    """

    template_name = "raffles/finish_raffle.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TicketListView(LoginRequiredMixin, DetailView):
    """
    View to list all the tickets generated for a raffle.
    """

    template_name = "raffles/list_tickets.html"
    model = RaffleModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # breakpoint()

        context["tickets"] = self.object.tickets.all()
        context["formset"] = formset_factory(TicketListForm, extra=1)

        context["raffle"] = self.object
        return context

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)

    #     return self.render_to_response(context)


class RaffleListPublicView(TemplateView):
    """
    View used to list all the raffles that are public.
    """

    template_name = "raffles/list_public_raffle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["raffles"] = RaffleModel.objects.filter(is_public=True)
        return context

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     context["raffles"] = RaffleModel.objects.filter(public=True)
