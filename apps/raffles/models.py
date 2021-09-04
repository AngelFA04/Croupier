from django.db import models


class RaffleModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Descripcion")
    start_date = models.DateTimeField(verbose_name="Fecha de inicio")
    end_date = models.DateTimeField(verbose_name="Fecha de fin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey("organizers.OrganizerModel", verbose_name="Organizador", on_delete=models.CASCADE, related_name="raffles")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "raffles"
        verbose_name = "Rifa"
        verbose_name_plural = "Rifas"


class TicketModel(models.Model):
    """
    Model for a raffle ticket.
    """

    price = models.DecimalField(max_digits=6, decimal_places=2)
    raffle = models.ForeignKey(RaffleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.raffle.name

    class Meta:
        db_table = "tickets"
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
