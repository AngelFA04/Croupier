from django import forms
from django.forms.widgets import HiddenInput
from raffles.models import RaffleModel
from raffles.models import TicketModel


class RaffleCreateForm(forms.ModelForm):
    """A form for creating a raffle"""

    organizer = forms.CharField(max_length=100, widget=HiddenInput, required=False)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Fecha de inicio"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Fecha de termino"
    )

    class Meta:
        model = RaffleModel
        fields = ["name", "description", "start_date", "end_date", "ticket_price"]

    def clean(self):
        if self.data["start_date"] > self.data["end_date"]:
            raise forms.ValidationError(
                "La fecha de inicio debe ser antes de la fecha final"
            )
        return super().clean()

    def save(self):
        self.instance.organizer = self.initial["organizer"]
        return super().save()


class RaffleDetailForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
        max_length=100,
        required=False,
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
        max_length=100,
        required=False,
    )
    start_date = forms.DateField(disabled=True, required=False)
    end_date = forms.DateField(disabled=True, required=False)
    is_public = forms.BooleanField(required=False, disabled=True)
    status = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
        max_length=100,
        required=False,
    )
    max_tickets = forms.IntegerField(disabled=True)
    min_tickets = forms.IntegerField(disabled=True)
    ticket_price = forms.DecimalField(disabled=True)

    class Meta:
        model = RaffleModel
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "is_public",
            "status",
            "max_tickets",
            "min_tickets",
            "ticket_price",
        ]


class RaffleUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(widget=forms.DateInput(), required=False)
    end_date = forms.DateField(required=False)
    # is_public = forms.BooleanField(required=False)
    status = forms.CharField(max_length=100, required=False)
    max_tickets = forms.IntegerField()
    min_tickets = forms.IntegerField()
    ticket_price = forms.DecimalField()

    class Meta:
        model = RaffleModel
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            # "is_public",
            "status",
            "max_tickets",
            "min_tickets",
            "ticket_price",
        ]


class RafflePublicateForm(RaffleDetailForm):
    """
    Form used to validate the publication of a raffle.
    """

    is_public = forms.BooleanField(widget=forms.HiddenInput)
    status = forms.CharField(widget=forms.HiddenInput)
    confirmation = forms.BooleanField(
        required=True,
        label="Confirmar",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Estoy seguro que los datos de la rifa son correctos y acepto su publicación",
    )

    def clean(self):
        if not self.cleaned_data["confirmation"]:
            raise forms.ValidationError("Debe confirmar la publicación")
        return super().clean()

    class Meta:
        model = RaffleModel
        fields = fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "max_tickets",
            "min_tickets",
            "ticket_price",
        ] + ["confirmation"]

    def save(self):
        self.instance.is_public = True
        self.instance.status = "Publicada"
        self.instance.save()
        return self.instance


class TicketListForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ["id", "is_sold", "is_paid"]
