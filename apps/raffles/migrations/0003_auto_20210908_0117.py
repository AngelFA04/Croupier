# Generated by Django 3.2.6 on 2021-09-08 06:17
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("raffles", "0002_auto_20210827_0753"),
    ]

    operations = [
        migrations.AddField(
            model_name="rafflemodel",
            name="is_public",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="rafflemodel",
            name="max_tickets",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="rafflemodel",
            name="min_tickets",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="rafflemodel",
            name="ticket_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]