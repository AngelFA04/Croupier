from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from raffles.forms import RaffleCreateForm
from raffles.forms import RaffleDetailForm
from raffles.forms import RafflePublicateForm
from raffles.forms import RaffleUpdateForm
from raffles.forms import TicketBuyForm
from raffles.forms import TicketListForm
from raffles.models import RaffleModel
from raffles.models import TicketModel


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

    def post(self, request, *args, **kwargs):
        data = request.POST
        # Change all tickets to not paid
        tickets = TicketModel.objects.filter(raffle=kwargs["pk"])
        tickets.update(is_paid=False)

        # Change the selected tickets to paid
        for key, value in data.items():
            if key.startswith("ticket_"):
                ticket_pk = key.split("_")[3]
                ticket = TicketModel.objects.get(pk=ticket_pk)
                ticket.is_paid = bool(value)
                ticket.save()

        return redirect("list-ticket", pk=kwargs["pk"])

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


class TicketEditView(LoginRequiredMixin, DetailView):
    """
    View to edit all the tickets generated for a raffle.
    """

    template_name = "raffles/edit_tickets.html"
    model = RaffleModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # breakpoint()

        context["tickets"] = self.object.tickets.all()
        context["formset"] = formset_factory(TicketListForm, extra=1)

        context["raffle"] = self.object
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        formset = context["formset"](request.POST)
        context["formset"] = formset
        if formset.is_valid():
            formset.save()
            return redirect("list-tickets", pk=self.object.pk)
        else:
            return self.render_to_response(context)


class TicketBuyView(DetailView):
    """
    View to buy tickets generated for a raffle.
    """

    template_name = "raffles/buy_tickets.html"
    model = RaffleModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # breakpoint()

        context["tickets"] = self.object.tickets.filter()
        context["formset"] = formset_factory(TicketListForm, extra=1)

        context["raffle"] = self.object
        return context


class TicketBuyDetailView(DetailView):
    """
    View to buy a ticket generated for a raffle.
    """

    template_name = "raffles/buy_ticket_detail.html"
    model = TicketModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = formset_factory(TicketListForm, extra=1)
        context["form"] = TicketBuyForm(instance=self.object)
        context["raffle"] = context["object"].raffle
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = TicketBuyForm(request.POST, instance=self.object)
        context["form"] = form
        if form.is_valid():
            form.save()
            # breakpoint()
            url = reverse("success-buyed-ticket", kwargs={"pk": self.object.pk})
            url += f"?code={self.object.code}"

            # return redirect(f"tickets/{self.object.id}?code={self.object.code}") # , pk=self.object.pk, kwargs={"code": self.object.code})
            return redirect(url)
        else:
            context["form"] = form
            return self.render_to_response(context)


def ticket_buyed_detail(request, pk):
    """
    View to show the information of the ticket that was buyed.
    """
    # Validate param code sent
    ticket = get_object_or_404(TicketModel, pk=pk)
    code = request.GET.get("code")

    if code != ticket.code:
        return HttpResponse("Invalid code", status=400)

    context = {}
    context["ticket"] = ticket
    context["code"] = code

    return render(request, "raffles/ticket_buyed_detail.html", context=context)
