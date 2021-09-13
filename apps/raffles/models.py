import datetime

from django.core.exceptions import ValidationError
from django.db import models


class RaffleStatuses(models.TextChoices):
    """
    Raffle statuses
    """

    PENDING = "pending", "Pendiente"
    ACTIVE = "completed", "Activa"
    CANCELED = "cancelled", "Cancelada"
    FINISHED = "finished", "Terminada"


class RaffleModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    max_tickets = models.IntegerField(default=0)
    min_tickets = models.IntegerField(default=0)
    ticket_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Precio de boleto"
    )
    # max_tickets_per_person = models.IntegerField(default=0)
    status = models.CharField(
        max_length=220, default="pending", choices=RaffleStatuses.choices
    )
    is_public = models.BooleanField(default=False)

    organizer = models.ForeignKey(
        "organizers.OrganizerModel",
        verbose_name="Organizador",
        on_delete=models.CASCADE,
        related_name="raffles",
    )

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        errors = {}
        if self.min_tickets > self.max_tickets:
            errors["min_tickets"] = "El minimo de tickets no puede ser mayor al maximo"

        start_date = self.start_date
        if start_date < datetime.date.today():
            errors["start_date"] = "Fecha de inicio debe ser mayor que hoy"

        end_date = self.end_date
        if end_date <= self.start_date:
            errors["end_date"] = "Fecha de fin debe ser mayor que fecha de inicio"

        if self.ticket_price <= 0:
            errors["ticket_price"] = "El precio debe ser mayor a 0"

        if self.max_tickets <= 0:
            errors["max_tickets"] = "El maximo de tickets debe ser mayor a 0"

        if errors:
            raise ValidationError(errors)
        # return super().clean_fields(exclude)

    # def clean(self) -> None:
    #     if self.min_tickets > self.max_tickets:
    #         raise ValidationError("El minimo de tickets no puede ser mayor al maximo")
    #     return super().clean()

    class Meta:
        db_table = "raffles"
        verbose_name = "Rifa"
        verbose_name_plural = "Rifas"


class TicketModel(models.Model):
    """
    Model for a raffle ticket.
    """

    # price = models.DecimalField(max_digits=6, decimal_places=2)
    identifier = models.CharField(
        max_length=100, verbose_name="Identificador"
    )  # TODO Change identifier???
    raffle = models.ForeignKey(
        RaffleModel, on_delete=models.CASCADE, related_name="tickets"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # TODO DELETE??
    is_sold = models.BooleanField(default=False, verbose_name="Vendidor")
    is_winner = models.BooleanField(default=False, verbose_name="Ganador")
    is_paid = models.BooleanField(default=False, verbose_name="Pagado")
    comments = models.TextField(blank=True, null=True)
    # qr_code = models.ImageField(upload_to="qr_codes", blank=True, null=True) TODO Implement

    def __str__(self):
        return self.raffle.name

    class Meta:
        db_table = "tickets"
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"
