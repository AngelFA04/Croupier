# Generated by Django 3.2.6 on 2021-09-08 06:29
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("raffles", "0003_auto_20210908_0117"),
    ]

    operations = [
        migrations.AddField(
            model_name="rafflemodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pendiente"),
                    ("completed", "Activa"),
                    ("cancelled", "Cancelada"),
                    ("finished", "Terminada"),
                ],
                default="pending",
                max_length=220,
            ),
        ),
        migrations.AlterField(
            model_name="rafflemodel",
            name="name",
            field=models.CharField(max_length=220),
        ),
    ]