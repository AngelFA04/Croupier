from django.contrib import admin
from raffles import models


# Register your models here.
@admin.register(models.RaffleModel)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "end_date", "status")
    list_filter = ("status",)
    search_fields = ("name", "description")


@admin.register(models.TicketModel)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("identifier", "raffle", "is_sold", "is_active")
    list_filter = (
        "is_sold",
        "is_active",
    )
