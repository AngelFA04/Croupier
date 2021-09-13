from django.db import models


class OrganizerModel(models.Model):
    """
    Model to store the organizer info of a user to show it publically.
    """

    user = models.OneToOneField(
        "users.UserModel", on_delete=models.CASCADE, related_name="organizer"
    )
    nickname = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="organizers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

    def getDescription(self):
        return self.description

    class Meta:
        db_table = "organizador"
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadores"
