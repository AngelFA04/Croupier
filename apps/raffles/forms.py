from django import forms
from django.forms.widgets import HiddenInput
from raffles.models import RaffleModel


class RaffleCreateForm(forms.ModelForm):
    """A form for creating a raffle"""

    organizer = forms.CharField(max_length=100, widget=HiddenInput, required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}),label="Fecha de inicio")
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}),label="Fecha de termino")

    class Meta:
        model = RaffleModel
        fields = ["name", "description", "start_date", "end_date"]

    def clean(self):
        if self.data["start_date"] > self.data["end_date"]:
            raise forms.ValidationError("La fecha de inicio debe ser antes de la fecha final")
        return super().clean()

    def save(self):
        self.instance.organizer = self.initial["organizer"]
        return super().save()
